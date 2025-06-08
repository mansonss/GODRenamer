
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
        name_to_id[game_name_clean.lower()] = title_id

def search_loop():
    while True:
        print("\nDo you want to search for a game name or title ID?")
        print("1 - Search by Game Name")
        print("2 - Search by Title ID")
        print("3 - Rename folders")
        print("4 - Exit")
        choice = input("Enter 1, 2, 3, or 4: ").strip()

        if choice == '1':
            name_query = input("Enter part of the game name to search for: ").lower()
            results = [name for name in name_to_id if name_query in name]
            if results:
                for name in results:
                    print(f"{name_to_id[name]} = {name}")
            else:
                print("No match found.")
        elif choice == '2':
            id_query = input("Enter Title ID (e.g. 415608C3): ").strip().upper()
            if id_query in id_to_name:
                print(f"{id_query} = {id_to_name[id_query]}")
            else:
                print("No match found.")
        elif choice == '3':
            rename_folders()
        elif choice == '4':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Try again.")

def rename_folders():
    print("Choose rename direction:")
    print("1 - Title ID -> Game Name [Title ID]")
    print("2 - Game Name [Title ID] -> Title ID")
    direction_choice = input("Enter 1 or 2: ").strip()
    direction = 'to_name' if direction_choice == '1' else 'to_id' if direction_choice == '2' else None

    if direction is None:
        print("Invalid rename choice. Returning to main menu.")
        return

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

search_loop()
