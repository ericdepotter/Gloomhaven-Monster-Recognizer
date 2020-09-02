import cv2
import datetime
import matplotlib.pyplot as pl
from mrcnn import utils
from mrcnn import visualize
import mrcnn.model as modellib
from mrcnn.config import Config
import numpy as np
import os

MODEL_DIR = r"E:\Generated\MaskRCNN"
WEIGHTS_PATH = r"E:\Generated\MaskRCNN\gloomhaven monster recognizer20200824T2144\mask_rcnn_gloomhaven monster recognizer_0010.h5"
VIDEO_DIRECTORY = r"E:\wetransfer-1b42bc"

class_names = ['ancient_artillery', 'bandit_archer', 'bandit_guard', 'black_imp', 'cave_bear', 'city_archer',
               'city_guard', 'cultist', 'deep_terror', 'earth_demon', 'flame_demon', 'forest_imp', 'frost_demon',
               'giant_viper', 'harrower_infester', 'hound', 'inox_archer', 'inox_guard', 'inox_shaman', 'living_bones',
               'living_corpse', 'living_spirit', 'lurker', 'night_demon', 'ooze', 'savvas_icestorm', 'savvas_lavaflow',
               'spitting_drake', 'stone_golem', 'sun_demon', 'vermling_scout', 'vermling_shaman', 'vicious_drake',
               'wind_demon']

monster_colors = {
    "ancient_artillery": (27.1, 35.3, 39.2),
    "bandit_archer": (71.8, 11, 11),
    "bandit_guard": (92.5, 25.1, 47.8),
    "black_imp": (53.3, 5.5, 31),
    "cave_bear": (77.3, 6.3, 38.4),
    "city_archer": (80.8, 57.6, 84.7),
    "city_guard": (55.7, 14.1, 66.7),
    "cultist": (29, 7.8, 54.9),
    "deep_terror": (23.9, 35.3, 99.6),
    "earth_demon": (16.1, 71.4, 96.5),
    "flame_demon": (0, 59.2, 65.5),
    "forest_imp": (9.4, 100, 100),
    "frost_demon": (0, 30.2, 25.1),
    "giant_viper": (50.6, 78, 51.8),
    "harrower_infester": (22, 55.7, 23.5),
    "hound": (0, 90.2, 46.3),
    "inox_archer": (54.5, 76.5, 29.0),
    'inox_guard': (46.3, 100, 0.8),
    "inox_shaman": (86.3, 90.6, 45.9),
    "living_bones": (66.6, 70.6, 16.9),
    "living_corpse": (51, 46.7, 9),
    "living_spirit": (93.3, 100, 25.5),
    "lurker": (100, 94.5, 46.3),
    "night_demon": (98.4, 75.3, 17.6),
    "ooze": (96.1, 49.8, 9),
    "savvas_icestorm": (82.4, 29, 0),
    "savvas_lavaflow": (100, 54.1, 39.6),
    "spitting_drake": (74.9, 21.2, 4.7),
    "stone_golem": (63.1, 53.3, 49.8),
    "sun_demon": (42.7, 29.8, 25.5),
    "vermling_scout": (30.6, 20.4, 18),
    "vermling_shaman": (62, 62, 62),
    "vicious_drake": (38, 38, 38),
    "wind_demon": (47.1, 56.5, 61.2)
}


class InferenceConfig(Config):
    # Give the configuration a recognizable name
    NAME = "Gloomhaven Monster Recognizer"

    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + len(class_names)  # Background + parcels

    IMAGE_RESIZE_MODE = "square"
    #IMAGE_MIN_DIM = 640
    #IMAGE_MAX_DIM = 896


def visualise(image, result):
    masked_image = image.copy()

    for idx, class_id in enumerate(result['class_ids']):
        clazz = class_names[class_id - 1]
        color = np.array(np.array(monster_colors[clazz]) * 2.55, dtype=image.dtype).tolist()

        mask = np.array(result['masks'][:, :, idx], dtype=image.dtype)
        mask_rgb = np.dstack([mask * 0.4] * 3)
        #mask_rgb[np.where((mask_rgb == [255, 255, 255]).all(axis=2))] = color

        color_image = np.zeros(image.shape, dtype=image.dtype)
        color_image[:] = color

        masked_image = np.array(masked_image * (1 - mask_rgb) + color_image * mask_rgb, dtype=image.dtype)

        y1, x1, y2, x2 = result['rois'][idx]
        try:
            cv2.rectangle(masked_image, (x1, y1), (x2, y2), color, 2)
        except TypeError:
            pass

        score = result['scores'][idx] if result['scores'] is not None else None
        caption = "{} {:.3f}".format(clazz, score) if score else clazz

        cv2.putText(masked_image, caption, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

    return masked_image

config = InferenceConfig()
config.display()

model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR,
                          config=config)

# Load weights
#weights_path = model.find_last()
print("Loading weights ", WEIGHTS_PATH)
model.load_weights(WEIGHTS_PATH, by_name=True)

for (dirpath, dirnames, filenames) in os.walk(VIDEO_DIRECTORY):
    for filename in filenames:
        video_path = os.path.join(dirpath, filename)

        # Video capture
        vcapture = cv2.VideoCapture(video_path)
        width = int(vcapture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vcapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = vcapture.get(cv2.CAP_PROP_FPS)

        print(width, height, fps)

        # Define codec and create video writer
        result_file = os.path.join(dirpath, filename.replace(".mkv", "_processed.avi"))
        vwriter = cv2.VideoWriter(result_file,
                                  cv2.VideoWriter_fourcc(*'MJPG'),
                                  fps, (width, height))

        count = 0
        success = True
        while success:
            print("frame: ", count)
            # Read next image
            success, image = vcapture.read()
            if success:
                # OpenCV returns images as BGR, convert to RGB
                real_image = image[..., ::-1]
                # Detect objects
                results = model.detect([real_image], verbose=0)

                # Display results
                masked_image = visualise(image, results[0])
                cv2.imshow(filename, masked_image)
                cv2.waitKey(1)

                # RGB -> BGR to save image to video
                masked_image = masked_image[..., ::-1]
                # Add image to video writer
                vwriter.write(masked_image)
                count += 1

        cv2.destroyAllWindows()
        vwriter.release()
        vcapture.release()