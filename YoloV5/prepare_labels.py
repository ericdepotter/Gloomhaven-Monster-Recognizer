import csv
import os

monsters = ['ancient_artillery', 'bandit_archer', 'bandit_guard', 'black_imp', 'cave_bear', 'city_archer', 'city_guard',
            'cultist', 'deep_terror', 'earth_demon', 'flame_demon', 'forest_imp', 'frost_demon', 'giant_viper',
            'harrower_infester', 'hound', 'inox_archer', 'inox_guard', 'inox_shaman', 'living_bones', 'living_corpse',
            'living_spirit', 'lurker', 'night_demon', 'ooze', 'savvas_icestorm', 'savvas_lavaflow', 'spitting_drake',
            'stone_golem', 'sun_demon', 'vermling_scout', 'vermling_shaman', 'vicious_drake', 'wind_demon']

#width = 1162.353
#height = 519.274

width=1920
height=1080

labels_dir = "E:/Generated/labels"

for (dirpath, dirnames, filenames) in os.walk(labels_dir):
    done = False
    for filename in filenames:
        path = dirpath + "/" + filename

        if not filename.endswith(".csv"):
            continue

        print(path)

        with open(path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')

            # Skip header
            next(reader)

            with open(path.replace("_bb.csv", ".txt"), 'w') as txt_file:
                for line in reader:
                    line[0] = monsters.index(line[0])
                    line[1] = float(line[1]) / width
                    line[2] = float(line[2]) / height
                    line[3] = float(line[3]) * 2 / width
                    line[4] = float(line[4]) * 2 / height

                    txt_file.write(" ".join(map(str, line)) + "\n")
