import os
import shutil
import warnings

# Paths to your folders
folder_A = '/Users/conniesun/Documents/pokemon_game/output/'
folder_B = '/Users/conniesun/Documents/pokemon_game/deleted_pokemons2/'
folder_C = '/Users/conniesun/Documents/pokemon_game/output_trimmed'

# Ensure folder C exists
if not os.path.exists(folder_C):
    os.makedirs(folder_C)

# List all files in Folder B
files_in_B = os.listdir(folder_B)

# Iterate over files in Folder B
for file_name in files_in_B:
    file_path_in_A = os.path.join(folder_A, file_name)
    
    # Check if the file exists in Folder A
    if os.path.exists(file_path_in_A):
        # Move the file from Folder A to Folder C
        shutil.move(file_path_in_A, folder_C)
    else:
        # File not found in Folder A, issue a warning
        warnings.warn(f"File {file_name} not found in Folder A.")
