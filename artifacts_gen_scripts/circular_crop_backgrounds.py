from PIL import Image, ImageDraw
import numpy as np
import os

# Function to create a circular crop of an image
def circular_crop(image_path, output_path, size, position):
    # Open the image file
    with Image.open(image_path).convert("RGBA") as img:
        # Calculate the position
        width, height = img.size
        left = (width - size) / 2 if position == 'center' else 0 if position in ['upper_left', 'lower_left'] else width - size
        upper = (height - size) / 2 if position == 'center' else 0 if position in ['upper_left', 'upper_right'] else height - size
        
        # Create mask for circular crop
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0, size, size), fill=255)

        # Crop the image
        img_cropped = img.crop((left, upper, left + size, upper + size))
        # Apply the mask to make the outside of the circle transparent
        img_cropped.putalpha(mask)

        # Save the new image
        img_cropped.save(output_path, 'PNG')


# Function to fill the correct lower part of the circular image with white
def fill_lower_part_with_white(image_path, output_path, fill_ratio):
    with Image.open(image_path) as img:
        # Get the dimensions of the image
        width, height = img.size
        # Calculate the height of the white fill within the circle
        fill_height = int(height * fill_ratio)

        # Create a white rectangle
        white_rect = Image.new('RGBA', (width, height), (250, 249, 246, 0))
        mask = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(mask)
        # Draw a full circle mask
        draw.ellipse((0, 0, width, height), fill)
        # Erase the top part of the circle to create the fill effect
        draw.rectangle([(0, 0), (width, height - fill_height)], fill=0)

        # Apply the mask to the white rectangle
        white_rect.putalpha(mask)

        # Combine the white lower circle with the original image
        combined = Image.alpha_composite(img, white_rect)

        # Save the modified image
        combined.save(output_path, 'PNG')



# Define the size of the circular crop
crop_size = 600

# Define the folder path containing the images
folder_path = '/Users/conniesun/Documents/pokemon_game/backgrounds'
output_folder_path = '/Users/conniesun/Documents/pokemon_game/backgrounds/cropped'

# Create the output folder if it does not exist
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# Ratio of the image's height to be filled with white
fill_ratio = 2/5

# Iterate over the images in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.png'):
        # Define the output path for the circular cropped image
        output_path_center = os.path.join(output_folder_path, f'{filename[:-4]}_center.png')
        output_path_upper_left = os.path.join(output_folder_path, f'{filename[:-4]}_upper_left.png')
        output_path_upper_right = os.path.join(output_folder_path, f'{filename[:-4]}_upper_right.png')
        output_path_lower_left = os.path.join(output_folder_path, f'{filename[:-4]}_lower_left.png')
        output_path_lower_right = os.path.join(output_folder_path, f'{filename[:-4]}_lower_right.png')

        # Perform the circular crop for each position
        circular_crop(os.path.join(folder_path, filename), output_path_center, crop_size, 'center')
        circular_crop(os.path.join(folder_path, filename), output_path_upper_left, crop_size, 'upper_left')
        circular_crop(os.path.join(folder_path, filename), output_path_upper_right, crop_size, 'upper_right')
        circular_crop(os.path.join(folder_path, filename), output_path_lower_left, crop_size, 'lower_left')
        circular_crop(os.path.join(folder_path, filename), output_path_lower_right, crop_size, 'lower_right')

        # Apply the white fill to the lower part of each circular cropped image
        fill_lower_part_with_white(output_path_center, output_path_center, fill_ratio)
        fill_lower_part_with_white(output_path_upper_left, output_path_upper_left, fill_ratio)
        fill_lower_part_with_white(output_path_upper_right, output_path_upper_right, fill_ratio)
        fill_lower_part_with_white(output_path_lower_left, output_path_lower_left, fill_ratio)
        fill_lower_part_with_white(output_path_lower_right, output_path_lower_right, fill_ratio)


# List the new files created
new_files = os.listdir(output_folder_path)
new_files_paths = [os.path.join(output_folder_path, file) for file in new_files]

new_files_paths
