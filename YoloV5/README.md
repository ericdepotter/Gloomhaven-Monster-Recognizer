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
	 
# Results

After training a ```YoloV5s```,  ```YoloV5m``` and  ```YoloV5x``` for respectively 5, 5.5 and 3 hours, it seems that the problem can be solved with the easiest model. This is great, since it allows for the fastest processing. Also note that for each model the ```best``` weights were also the ```last``` weights. This indicates that even better results can be obtained by training with more epochs. The resulting weights of these training sessions can be found in the folder ```weights```.


| Model         | Epochs | Img size | Precision | Recall | mAP@.5 | mAP@.5:.95 | Time (ms) |
|---------------|--------|----------|-----------|--------|--------|------------|-----------|
| YoloV5s       | 50     | 640      | 64.1%     | 99.7%  | 99.7%  | 94.1%      | 3.5       |
| YoloV5s       | 50     | 940      | 72.6%     | 99.8%  | 99.8%  | 95.5%      | 6.5       |
| YoloV5s (TTA) | 50     | 940      | 51.6%     | 99.9%  | 99.4%  | 94.9%      | 13.5      |
| YoloV5m       | 50     | 640      | 63.5%     | 99.8%  | 99.4%  | 96.4%      | 6.3       |
| YoloV5m       | 50     | 940      | 71.6%     | 100%   | 99.5%  | 97.2%      | 12.9      |
| Yolov5m (TTA) | 50     | 940      | 51.5%     | 100%   | 99.5%  | 96.7%      | 27.7      |
| YoloV5x       | 10     | 640      | 63.6%     | 99.6%  | 99.3%  | 94.3%      | 17.4      |
| YoloV5x       | 10     | 940      | 70.4%     | 99.9%  | 99.4%  | 94.9%      | 38.1      |
| YoloV5x (TTA) | 10     | 940      | 50%       | 100%   | 99.5%  | 94.8%      | 86.7      |