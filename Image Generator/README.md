# Image Generator

To have enough images to train a CNN without the need to manually place the monsters on a tile, take a picture and annotate the image, I opted to build a synthetic dataset. For this purpose I used Unreal Engine 4 as it allows for easy setup and rendering of a 3D-scene.

The generation process uses multiple camera to capture the monsters from different heights and angles. To further increase the variability, randomness is introduced in the angle towards the camera, placing the monsters on the tiles, the relative position and angle of the monster and its standee and the texture used for representing the underlying table.

## Usage
Open the project in Unreal Engine 4. The project was build with version 4.25.1. Press play and in-game press ```e``` to start generating the images. The images and their corresponding masks will be stored in ```<GAME_DIRECTORY>/Saved/Screenshots/```.

### Configuration
To configure the generation open the level blueprint. Next set the parameters at the beginning of the ```BeginPlay``` node:

![Generation parameters](https://raw.githubusercontent.com/ericdepotter/Gloomhaven-Monster-Recognizer/master/Image%20Generator/Generation%20parameters.png)

  * **Is Train**: Will store the generated images and masks in the ```train``` subfolder if the value is ```true```. Otherwise they are stored in the ```val``` subfolder.
  * **Start Index**: The start-index for the loop. The image name will begin from ```Start Index + 1```.
  * **Amount**: The number of images to generate.