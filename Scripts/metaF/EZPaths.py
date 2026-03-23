from pathlib import Path
import os # os module still needed for chdir

# Get the absolute path of the directory containing the script
script_dir = Path(__file__).parent.resolve()
script_dir = str(script_dir).split('/')
path = '/'
for i in range(1,len(script_dir)-1):
    path += script_dir[i] + '/'

The_Dungeon_Path = path
# print(path == "/home/tej/Desktop/Code_Stuff/Repositories/pro_dragon/The_Dungeon_of_the_Dragon/Scripts/")

# The_Dungeon_Path = "/home/tej/Desktop/Code_Stuff/Repositories/pro_dragon/The_Dungeon_of_the_Dragon/Scripts/"
# Weapon_Path = The_Dungeon_Path + "txtFiles/allWeapons/baseWeapons.txt"


Saves_Path = "/home/tej/Desktop/TestSave1/"