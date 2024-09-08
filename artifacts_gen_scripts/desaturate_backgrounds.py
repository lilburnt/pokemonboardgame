from PIL import Image, ImageEnhance
import os

# Define the directory containing the PNG files
directory = '/Users/conniesun/Documents/pokemon_game/backgrounds_original'

# Function to desaturate an image
def desaturate_image(file_path, desaturation_level=0.4):
    # Open the image
    img = Image.open(file_path)

    # If the image has an alpha channel, split it and temporarily remove it
    if img.mode == 'RGBA':
        alpha = img.split()[-1]
        img = img.convert('RGB')
    else:
        alpha = None

    # Convert to HSV, desaturate and convert back to RGB
    hsv_img = img.convert('HSV')
    h, s, v = hsv_img.split()
    s = ImageEnhance.Brightness(s).enhance(desaturation_level)
    desaturated_img = Image.merge('HSV', (h, s, v)).convert('RGB')

    # Re-apply the alpha channel if it was present
    if alpha:
        desaturated_img.putalpha(alpha)

    # Save the desaturated image
    desaturated_file_path = f'/Users/conniesun/Documents/pokemon_game/backgrounds/{os.path.basename(file_path)}'
    desaturated_img.save(desaturated_file_path)

    return desaturated_file_path

# Iterate over all PNG files in the directory and desaturate them
desaturated_file_paths = []
for filename in os.listdir(directory):
    if filename.lower().endswith('.png'):
        file_path = os.path.join(directory, filename)
        desaturated_file_path = desaturate_image(file_path)
        desaturated_file_paths.append(desaturated_file_path)

print(desaturated_file_paths)
