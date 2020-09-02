import os

current_dir = os.path.dirname(__file__)
images_dir = os.path.join(current_dir, '../Images/Monsters/Prepped')

monsters = []
for (dirpath, dirnames, filenames) in os.walk(images_dir):
    monsters.extend([filename.replace(".png", "") for filename in filenames])
    break

print(len(monsters), monsters)