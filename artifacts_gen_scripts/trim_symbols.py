import os
from PIL import Image

# Path to the symbols directory
symbols_dir = '/Users/conniesun/Documents/pokemon_game/symbols/'

# Function to trim the extra edges of an image based on the alpha channel
def trim_image(image_path):
    image = Image.open(image_path)
    
    # Convert to RGBA if necessary to ensure there's an alpha channel
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    
    # Get the bounding box
    bbox = image.getbbox()
    
    # Crop the image to the bounding box
    trimmed_image = image.crop(bbox)
    return trimmed_image

# Loop through all the files in the folder
for file_name in os.listdir(symbols_dir):
    if file_name.endswith('.png'):
        file_path = os.path.join(symbols_dir, file_name)
        # Trim the image
        trimmed_image = trim_image(file_path)
        
        # Save the trimmed image
        trimmed_file_path = os.path.join(symbols_dir, f"trimmed_{file_name}")
        trimmed_image.save(trimmed_file_path)