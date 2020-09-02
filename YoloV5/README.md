# Content

Configuration files and code to prepare the data for the YoloV5 algorithm as implemented by [ultralytics](https://github.com/ultralytics/yolov5)

Folder contents:

  * **coco.yaml**: A description of the dataset used for training the model.
  * **list_monster_names.py**: List all the monsters that are found in the masks folder.
  * **prepare_labels.py (deprecated)**: In a previous attempt, I tried to generate the bounding boxes in UE4 itself. However this attempt was unsuccessfull.
  * **prepare_labels_from_masks.py**: Obtains the bounding boxes from the masks and outputs the labels in the format required for training the YoloV5 model. The labels are stored in the path of the image with ```images``` replaced by ```labels```.
  * **yolo_visualize.py**: Visualize the dataset (images and bounding boxes).
  * **yolov5x.yaml**: The YoloV5x model with the correct number of classes.

# Instructions

To train a YoloV5 model:

  1. Choose a model config and set the correct number of classes.
  1. Install YoloV5. Perform the first step from the [training guide](https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data).
  1. Set the correct paths to the train and validation images in ```coco.yaml```.
  1. Run the following command (assumes YoloV5 in installed in the folder and the command is executed in the yolov5-x.y subfolder):
  
     ```python train.py  --batch 4 --epochs 10 --cfg ../yolov5x.yaml --data ../coco.yaml --weight yolov5x.pt```