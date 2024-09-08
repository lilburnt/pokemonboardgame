import os

# Set the directory where your files are located
directory = '/Users/conniesun/Documents/pokemon_game/output'

# Loop through all the files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".png") and '_' in filename:
        # Split the name by '_'
        parts = filename.split('_')
        # Check if the part before '_' is non-empty and the part after '_' is numeric
        if parts[0] and parts[1].replace('.png', '').isdigit():
            # Construct the new filename without '_n'
            new_filename = parts[0] + '.png'
            # Rename the file
            os.rename(os.path.join(directory, filename), os.path.join(directory, new_filename))
            print(f'Renamed "{filename}" to "{new_filename}"')

print("Renaming complete.")
