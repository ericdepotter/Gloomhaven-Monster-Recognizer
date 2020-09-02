import cv2
import numpy as np
import os

labels_dir = "D:/Generated/labels"

class_names = ['ancient_artillery', 'bandit_archer', 'bandit_guard', 'black_imp', 'cave_bear', 'city_archer', 'city_guard',
            'cultist', 'deep_terror', 'earth_demon', 'flame_demon', 'forest_imp', 'frost_demon', 'giant_viper',
            'harrower_infester', 'hound', 'inox_archer', 'inox_guard', 'inox_shaman', 'living_bones', 'living_corpse',
            'living_spirit', 'lurker', 'night_demon', 'ooze', 'savvas_icestorm', 'savvas_lavaflow', 'spitting_drake',
            'stone_golem', 'sun_demon', 'vermling_scout', 'vermling_shaman', 'vicious_drake', 'wind_demon']

class_colors = {
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


for (dirpath, dirnames, filenames) in os.walk(labels_dir):
    for filename in filenames:
        path = dirpath + "/" + filename

        if not filename.endswith(".txt"):
            continue

        with open(path, 'r') as file:
            img_path = path.replace("labels", "images").replace(".txt", ".png")
            print(img_path)
            img = cv2.imread(img_path)
            height, width, channels = img.shape

            for line in file.readlines():
                line = line.split(" ")

                clazz = class_names[int(line[0])]
                color = np.array(np.array(class_colors[clazz]) * 2.55, dtype=np.uint8).tolist()

                center = [
                    float(line[1]) * width,
                    float(line[2]) * height
                ]
                label_width = float(line[3]) * width
                label_height = float(line[4]) * height

                top_left = (round(center[0] - label_width/2), round(center[1] - label_height/2))
                bot_right = (round(center[0] + label_width/2), round(center[1] + label_height/2))

                img = cv2.rectangle(img, top_left, bot_right, color, 2)

                caption = clazz
                cv2.putText(img, caption, (top_left[0], top_left[1] - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

            cv2.imshow("Image", img)
            cv2.waitKey(0)