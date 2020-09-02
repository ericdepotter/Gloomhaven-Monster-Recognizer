from collections import defaultdict
import cv2
from functools import partial
from multiprocessing import Pool
import os
import re

IMAGE_DIRECTORY = r"E:\Generated\images"
MASK_DIRECTORY = r"E:\Generated\masks"

monsters = ['ancient_artillery', 'bandit_archer', 'bandit_guard', 'black_imp', 'cave_bear', 'city_archer', 'city_guard',
            'cultist', 'deep_terror', 'earth_demon', 'flame_demon', 'forest_imp', 'frost_demon', 'giant_viper',
            'harrower_infester', 'hound', 'inox_archer', 'inox_guard', 'inox_shaman', 'living_bones', 'living_corpse',
            'living_spirit', 'lurker', 'night_demon', 'ooze', 'savvas_icestorm', 'savvas_lavaflow', 'spitting_drake',
            'stone_golem', 'sun_demon', 'vermling_scout', 'vermling_shaman', 'vicious_drake', 'wind_demon']

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080

MASK_REGEX = r"image_\d+_mask_\d+_(.*)\.png"


def get_mask_contours(image_id, image_masks, debug=False):
    image_id_filter = image_id + "_"
    image_masks = [x for x in image_masks if image_id_filter in x[1]]

    result = []

    if debug:
        print("{}: {}".format(image_id, image_masks))

    mask_id = 0
    for (dirpath, filename) in image_masks:
        mask = cv2.imread(os.path.join(dirpath, filename))
        name = re.match(MASK_REGEX, filename)[1]

        gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour = sorted(contours, key=lambda x: -cv2.contourArea(x))[0]

        result.append((name, contour))

        if debug:
            cv2.drawContours(mask, contours, -1, (0, 255, 0), thickness=1)
            cv2.drawContours(mask, [contour], -1, (0, 0, 255), thickness=2)
            cv2.imshow("{}: {} - {}".format(image_id, mask_id, name), mask)

        mask_id += 1

    if debug:
        print([x[0] for x in result])
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return result


def process_image(image, image_masks):
    dirpath, filename = image
    image_id = filename.replace(".png", "")

    try:
        sub_masks = get_mask_contours(image_id, image_masks)
    except IndexError:
        print("Error processing image: " + image_id)
        return None

    class_count = defaultdict(lambda: 0)
    label_dir = dirpath.replace("images", "labels")
    if not os.path.exists(label_dir):
        os.makedirs(label_dir)

    label_filename = filename.replace(".png", ".txt")

    with open(os.path.join(label_dir, label_filename), 'w') as txt_file:
        for (name, sub_mask) in sub_masks:
            class_count[name] += 1
            top_left_x, top_left_y, w, h = cv2.boundingRect(sub_mask)

            line = [
                monsters.index(name),
                (top_left_x + w / 2) / IMAGE_WIDTH,
                (top_left_y + h / 2) / IMAGE_HEIGHT,
                w / IMAGE_WIDTH,
                h / IMAGE_HEIGHT
            ]

            txt_file.write(" ".join(map(str, line)) + "\n")

    return dict(class_count)


if __name__ == "__main__":
    masks = []
    for (dirpath, dirnames, filenames) in os.walk(MASK_DIRECTORY):
        for filename in filenames:
            if 'mask' not in filename:
                continue

            masks.append((dirpath, filename))

    image_names = []
    for (dirpath, dirnames, filenames) in os.walk(IMAGE_DIRECTORY):
        #if "train" in dirpath:
        #    print("Skipping train directory")
        #    continue

        for filename in filenames:
            image_names.append((dirpath, filename))

    processed_images = []

    #for idx in range(10):
    #    processed_images.append(process_image(image_names[idx], masks))

    with Pool(5) as pool:
        processed_images.extend(pool.map(partial(process_image, image_masks=masks), image_names))

    all_classes_found = defaultdict(lambda: 0)
    images_count = 0
    for el in processed_images:
        if el is None:
            continue

        images_count += 1

        for clazz, count in el.items():
            all_classes_found[clazz] += count

    print("")
    print("")
    print("{} successful images".format(images_count))

    print("\n\n== Classes found: {} ==".format(len(list(all_classes_found.keys()))))
    for key, value in all_classes_found.items():
        print("  - {}: {}".format(key, value))