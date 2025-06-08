
import os
import csv
import re

# Load CSV data using utf-8-sig to skip BOM
csv_path = "xbox360_gamelist.csv"
id_to_name = {}
name_to_id = {}

with open(csv_path, newline='', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        title_id = row['Title ID'].strip()
        game_name = row['Game Name'].strip()
        game_name_clean = re.sub(r'[<>:"/\\|?*]', '', game_name)
        id_to_name[title_id] = game_name_clean
        name_to_id[game_name_clean] = title_id

# Ask user for rename direction
print("Choose rename direction:")
print("1 - Title ID -> Game Name [Title ID]")
print("2 - Game Name [Title ID] -> Title ID")
choice = input("Enter 1 or 2: ").strip()

if choice == '1':
    direction = 'to_name'
elif choice == '2':
    direction = 'to_id'
else:
    print("Invalid choice. Exiting.")
    exit(1)

# Scan folder names in current directory
folders = [f for f in os.listdir('.') if os.path.isdir(f)]

for folder in folders:
    if direction == 'to_name':
        if folder in id_to_name:
            new_name = f"{id_to_name[folder]} [{folder}]"
            if not os.path.exists(new_name):
                print(f"Renaming {folder} -> {new_name}")
                os.rename(folder, new_name)
    elif direction == 'to_id':
        match = re.search(r'\[([0-9A-F]{8})\]$', folder)
        if not match:
            match = re.search(r'\[(.{8})\]$', folder)
        if match:
            title_id = match.group(1)
            if title_id in id_to_name and folder != title_id:
                print(f"Renaming {folder} -> {title_id}")
                os.rename(folder, title_id)
