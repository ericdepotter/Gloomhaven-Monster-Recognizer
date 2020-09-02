from collections import defaultdict
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import csv
import cv2
import json
from multiprocessing import Pool
import numpy as np
import os

monster_colors = {
    (0, 0, 0): "background",
    (27.1, 35.3, 39.2): "ancient_artillery",
    (71.8, 11, 11): "bandit_archer",
    (92.5, 25.1, 47.8): "bandit_guard",
    (53.3, 5.5, 31): "black_imp",
    (77.3, 6.3, 38.4): "cave_bear",
    (80.8, 57.6, 84.7): "city_archer",
    (55.7, 14.1, 66.7): "city_guard",
    (29, 7.8, 54.9): "cultist",
    (23.9, 35.3, 99.6): "deep_terror",
    (16.1, 71.4, 96.5): "earth_demon",
    (0, 59.2, 65.5): "flame_demon",
    (9.4, 100, 100): "forest_imp",
    (0, 30.2, 25.1): "frost_demon",
    (50.6, 78, 51.8): "giant_viper",
    (22, 55.7, 23.5): "harrower_infester",
    (0, 90.2, 46.3): "hound",
    (54.5, 76.5, 29.0): "inox_archer",
    (46.3, 100, 0.8): 'inox_guard',
    (86.3, 90.6, 45.9): "inox_shaman",
    (66.6, 70.6, 16.9): "living_bones",
    (51, 46.7, 9): "living_corpse",
    (93.3, 100, 25.5): "living_spirit",
    (100, 94.5, 46.3): "lurker",
    (98.4, 75.3, 17.6): "night_demon",
    (96.1, 49.8, 9): "ooze",
    (82.4, 29, 0): "savvas_icestorm",
    (100, 54.1, 39.6): "savvas_lavaflow",
    (74.9, 21.2, 4.7): "spitting_drake",
    (63.1, 53.3, 49.8): "stone_golem",
    (42.7, 29.8, 25.5): "sun_demon",
    (30.6, 20.4, 18): "vermling_scout",
    (62, 62, 62): "vermling_shaman",
    (38, 38, 38): "vicious_drake",
    (47.1, 56.5, 61.2): "wind_demon"
}

categories = list(monster_colors.values())
is_crowd = 0
all_monsters_found = defaultdict(lambda: 0)


def get_mask_contours(image, monsters_in_image, debug=False):
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 5, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    monster_contours = {}
    for i in range(len(contours)):
        # Create a mask image that contains the contour filled in
        cimg = np.zeros_like(imgray)
        cv2.drawContours(cimg, contours, i, color=255, thickness=-1)
        ret, thresh = cv2.threshold(cimg, 5, 255, 0)

        # Access the image pixels and create a 1D numpy array then add to list
        pts = np.where(cimg == 255)
        if len(pts[0]) < 500:
            continue

        counts = defaultdict(lambda: 0)
        for c in image[pts[0], pts[1]]:
            counts[tuple(c)] += 1

        unique_bgrs = [k for k in counts.keys() if counts[k] > 100]

        colors_per_monster = defaultdict(lambda: [])
        for bgr in unique_bgrs:
            closest_color = ()
            min_dist = 500000

            # Compute the closest color using the delta E metric
            # http://hanzratech.in/2015/01/16/color-difference-between-2-colors-using-python.html
            for color in monster_colors.keys():
                if monster_colors[color] not in monsters_in_image:
                    continue

                pixel_color = sRGBColor(bgr[2]/255, bgr[1]/255, bgr[0]/255)
                monster_color = sRGBColor(color[0]/100, color[1]/100, color[2]/100)

                # Convert from RGB to Lab Color Space
                pixel_color_lab = convert_color(pixel_color, LabColor)
                monster_color_lab = convert_color(monster_color, LabColor)

                delta_e = delta_e_cie2000(pixel_color_lab, monster_color_lab)

                if delta_e < min_dist:
                    min_dist = delta_e
                    closest_color = color

            # If the pixel is not black...
            if closest_color != (0, 0, 0):
                colors_per_monster[closest_color].append(bgr)

        for key, colors in colors_per_monster.items():
            colors = np.array(colors)
            min_color = np.min(colors, axis=0)
            max_color = np.max(colors, axis=0)

            mask = cv2.inRange(image, min_color, max_color)
            if cv2.countNonZero(mask) < 500:
                continue

            masked = cv2.bitwise_and(thresh, thresh, mask=mask)
            blurred = cv2.GaussianBlur(masked, (7, 7), 0)
            sub_contours, _ = cv2.findContours(blurred, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            monster_contours[key] = sorted(sub_contours, key=lambda x: -cv2.contourArea(x))[0]

            if debug:
                cv2.imshow(str(key), masked)

    if debug:
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return monster_contours


def create_sub_mask_annotation(sub_mask, image_id, category_id, annotation_id, is_crowd):
    segmentations = [cv2.approxPolyDP(sub_mask, 3, True)]
    bbox = cv2.boundingRect(segmentations[0])

    return {
        'segmentation': [s.ravel().tolist() for s in segmentations],
        'iscrowd': is_crowd,
        'image_id': image_id,
        'category_id': category_id,
        'id': annotation_id,
        'bbox': tuple(bbox),
        'area': cv2.contourArea(sub_mask)
    }


def process_image(image):
    dirpath, filename = image
    image_id = filename.replace("_mask", "").replace(".png", "")

    # Check bounding box information to see which monsters there are in this image
    monsters_in_image = []

    try:
        """
        with open(os.path.join(dirpath, image_id).replace("masks", "labels/train") + "_bb.csv", newline='') as bb_file:
            reader = csv.reader(bb_file)

            # Skip header
            next(reader)

            for line in reader:
                monsters_in_image.append(line[0])
        """

        with open(os.path.join(dirpath, image_id).replace("masks", "labels") + "_bb.txt", newline='') as bb_file:
            reader = csv.reader(bb_file)

            for line in reader:
                monsters_in_image.append(line[0])
    except FileNotFoundError:
        print(image_id + ": Bounding box information not found: skipping image")
        return None

    if len(monsters_in_image) > len(set(monsters_in_image)):
        print(image_id + ": Duplicate monsters found: skipping for safety.")
        return None

    image = cv2.imread(os.path.join(dirpath, filename))

    sub_masks = get_mask_contours(image, monsters_in_image)
    found_monsters = [monster_colors[c] for c in sub_masks.keys()]

    if sorted(monsters_in_image) != sorted(found_monsters):
        print(image_id + ": Not the same monsters found: skipping image")
        return None

    annotations = []
    annotation_id = 1
    for key, value in sub_masks.items():
        category_id = categories.index(monster_colors[key]) + 1
        annotation = create_sub_mask_annotation(
            value,
            image_id,
            category_id,
            image_id + "_" + str(annotation_id),
            is_crowd
        )
        annotations.append(annotation)
        annotation_id += 1

    return {
        'annotations': annotations,
        'image': {
            'id': image_id,
            # 'file_name': os.path.join(dirpath, image_id).replace("masks", "images") + ".png"
            'file_name': image_id + ".png"
        }
    }


if __name__ == "__main__":
    image_directory = r"E:\Generated\masks"
    image_names = []

    for (dirpath, dirnames, filenames) in os.walk(image_directory):
        if "val" in dirpath:
            print("Skipping val directory")
            continue

        for filename in filenames:
            if not 'mask' in filename:
                continue

            image_names.append((dirpath, filename))

    processed_images = []
    with Pool(5) as p:
        processed_images = p.map(process_image, image_names)

    annotations = []
    images = []
    for el in processed_images:
        if el is None:
            continue

        images.append(el["image"])
        annotations.extend(el["annotations"])

        for annotation in el["annotations"]:
            all_monsters_found[categories[annotation["category_id"] - 1]] += 1

    print("")
    print("")
    print("{} successful images".format(len(images)))

    print("\n\n== Monsters found: {} ==".format(len(list(all_monsters_found.keys()))))
    for key, value in all_monsters_found.items():
        print("  - {}: {}".format(key, value))

    coco = {
        'categories': [
            {
                'id': idx + 1,
                'name': cat,
                'supercategory': None
            }
            for idx, cat in enumerate(categories)
        ],
        'images': images,
        'annotations': annotations
    }

    with open(r"E:\Generated\annotations.json", "w") as file:
        json.dump(coco, file)