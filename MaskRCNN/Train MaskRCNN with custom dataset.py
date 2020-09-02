# TODO check for transfer learning: https://thebinarynotes.com/how-to-train-mask-r-cnn-on-the-custom-dataset/
# Source: https://github.com/miki998/Custom_Train_MaskRCNN/blob/master/train.py
import json
import cv2
import os
import numpy as np

# Import Mask RCNN
from mrcnn.config import Config
from mrcnn import model as modellib, utils

category = "monster"
class_names = ['ancient_artillery', 'bandit_archer', 'bandit_guard', 'black_imp', 'cave_bear', 'city_archer',
               'city_guard', 'cultist', 'deep_terror', 'earth_demon', 'flame_demon', 'forest_imp', 'frost_demon',
               'giant_viper', 'harrower_infester', 'hound', 'inox_archer', 'inox_guard', 'inox_shaman', 'living_bones',
               'living_corpse', 'living_spirit', 'lurker', 'night_demon', 'ooze', 'savvas_icestorm', 'savvas_lavaflow',
               'spitting_drake', 'stone_golem', 'sun_demon', 'vermling_scout', 'vermling_shaman', 'vicious_drake',
               'wind_demon']

# Synthetic
CONFIG = {
    "VALIDATION_SIZE": 497,
    "TRAINING_SIZE": 9500,

    "IMAGE_DIR": r"D:\Generated\images\train",
    "VALIDATION_DIR": r"D:\Generated\images\val",
    "ANNOTATIONS_FILE": r"D:\Generated\annotations.json",

    "MODEL_DIR": r"D:\Generated\MaskRCNN",
    "MASK_IMAGES": False
}


class CustomDataset(utils.Dataset):
    def load_custom(self, image_dir, annotations_file, subset):
        """
        Load a subset of the dataset.
        image_dir: Directory of the images.
        annotations_file: 
        subset: Subset to load: train or val
        """
        # Add classes. We have only one class to add.
        for i in range(1, len(class_names)+1):
            self.add_class(category, i, class_names[i-1])

        dataset = {}
        with open(annotations_file, "r") as file:
            dataset = json.load(file)

        images = dataset['images']
        annotations = dataset['annotations']

        start_index_validation = len(images) - CONFIG["VALIDATION_SIZE"]

        for idx, image in enumerate(images):
            polygons = []
            class_ids = []
            annotation_ids = []

            if subset == "val" and idx < start_index_validation:
                continue
            elif subset == "train" and idx >= CONFIG["TRAINING_SIZE"]:
                break

            image_annotations = [a for a in annotations if a['image_id'] == image['id']]

            # we are now inputting the polygons
            for image_annotation in image_annotations:
                polygons.append(image_annotation['segmentation'])
                class_ids.append(image_annotation['category_id'])
                annotation_ids.append(image_annotation['id'])

            self.add_image(
                category,
                image_id=image['file_name'],  # use file name as a unique image id
                path=os.path.join(image_dir, image['file_name']),
                width=1920,
                height=1080,
                polygons=polygons, 
                class_ids=class_ids,
                image_dir=image_dir,
                annotation_ids=annotation_ids
            )

    def load_mask(self, image_id):
        """
        Generate instance masks for an image.
        Returns:
        masks: A bool array of shape [height, width, instance count] with one mask per instance.
        class_ids: a 1D array of class IDs of the instance masks.
        """
        # If not an image of this dataset, delegate to parent class.
        image_info = self.image_info[image_id]
        if image_info["source"] != category:
            return super(self.__class__, self).load_mask(image_id)
        
        class_ids = image_info['class_ids']

        result = np.zeros((720, 1280, len(image_info["polygons"])),
                        dtype=np.uint8)

        if CONFIG["MASK_IMAGES"]:
            for idx, annotation_id in enumerate(image_info["annotation_ids"]):
                mask = cv2.imread(os.path.join(image_info["image_dir"], annotation_id + ".jpg"), cv2.IMREAD_GRAYSCALE)
                result[:, :, idx] = mask
        else:
            # Convert polygons to a bitmap mask of shape
            # [height, width, instance_count]
            for idx, p in enumerate(image_info["polygons"]):
                points = []
                for i in range(0, len(p[0]), 2):
                    points.append([p[0][i], p[0][i+1]])

                points = np.array(points, dtype=np.int32)
                try:
                    mask = np.zeros((720, 1280), dtype=np.uint8)
                    cv2.fillPoly(mask, [points], color=(255,255,255))
                    result[:, :, idx] = mask
                except Exception as e:
                    print("")
                    print("")
                    print("")
                    print("")
                    print(image_id, image_info, points)
                    raise e

        # Return mask, and array of class IDs of each instance. 
        class_ids = np.array(class_ids, dtype=np.int32)
        return result.astype(np.bool), class_ids

    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == category:
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)


def prepare_data():
    # Training dataset.
    print("Loading training data")
    dataset_train = CustomDataset()
    dataset_train.load_custom(CONFIG["IMAGE_DIR"], CONFIG["ANNOTATIONS_FILE"], "train")
    dataset_train.prepare()

    # Validation dataset
    print("Loading validation data")
    dataset_val = CustomDataset()
    dataset_val.load_custom(CONFIG["IMAGE_DIR"], CONFIG["ANNOTATIONS_FILE"], "val")
    dataset_val.prepare()

    return dataset_train, dataset_val


def train(model, dataset_train, dataset_val):
    """Train the model."""
    # *** This training schedule is an example. Update to your needs ***
    # Since we're using a very small dataset, and starting from
    # COCO trained weights, we don't need to train too long. Also,
    # no need to train all layers, just the heads should do it.
    print("Training network heads")
    """model.train(dataset_train, dataset_val,
                learning_rate=config.LEARNING_RATE,
                epochs=10,
                layers='heads')"""
    model.train(
        dataset_train,
        dataset_val,
        learning_rate=config.LEARNING_RATE,
        epochs=10,
        layers='heads'
    )


class CustomConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "Gloomhaven Monster Recognizer"

    # NUMBER OF GPUs to use. When using only a CPU, this needs to be set to 1.
    GPU_COUNT = 1

    # Number of images to train with on each GPU. A 12GB GPU can typically
    # handle 2 images of 1024x1024px.
    # Adjust based on your GPU memory and image sizes. Use the highest
    # number that your GPU can handle for best performance.
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + len(class_names)  # Background + parcels

    # Number of training steps per epoch
    STEPS_PER_EPOCH = CONFIG["TRAINING_SIZE"]
    VALIDATION_STEPS = CONFIG["VALIDATION_SIZE"]

    # Skip detections with < 75% confidence
    #DETECTION_MIN_CONFIDENCE = 0.75

    # Input image resizing
    # Generally, use the "square" resizing mode for training and predicting
    # and it should work well in most cases. In this mode, images are scaled
    # up such that the small side is = IMAGE_MIN_DIM, but ensuring that the
    # scaling doesn't make the long side > IMAGE_MAX_DIM. Then the image is
    # padded with zeros to make it a square so multiple images can be put
    # in one batch.
    # Available resizing modes:
    # none:   No resizing or padding. Return the image unchanged.
    # square: Resize and pad with zeros to get a square image
    #         of size [max_dim, max_dim].
    # pad64:  Pads width and height with zeros to make them multiples of 64.
    #         If IMAGE_MIN_DIM or IMAGE_MIN_SCALE are not None, then it scales
    #         up before padding. IMAGE_MAX_DIM is ignored in this mode.
    #         The multiple of 64 is needed to ensure smooth scaling of feature
    #         maps up and down the 6 levels of the FPN pyramid (2**6=64).
    # crop:   Picks random crops from the image. First, scales the image based
    #         on IMAGE_MIN_DIM and IMAGE_MIN_SCALE, then picks a random crop of
    #         size IMAGE_MIN_DIM x IMAGE_MIN_DIM. Can be used in training only.
    #         IMAGE_MAX_DIM is not used in this mode.
    IMAGE_RESIZE_MODE = "square"
    #IMAGE_MIN_DIM = 640
    #IMAGE_MAX_DIM = 896


if __name__ == "__main__":
    dataset_train, dataset_val = prepare_data()
    config = CustomConfig()
    model = modellib.MaskRCNN(mode="training", config=config, model_dir=CONFIG["MODEL_DIR"])

    # Download weights file
    weights_path = os.path.join(CONFIG["MODEL_DIR"], "mask_rcnn_coco.h5")
    utils.download_trained_weights(weights_path)

    # Exclude the last layers because they require a matching
    # number of classes
    model.load_weights(weights_path, by_name=True, exclude=[
        "mrcnn_class_logits", "mrcnn_bbox_fc",
        "mrcnn_bbox", "mrcnn_mask"])

    train(model, dataset_train, dataset_val)
