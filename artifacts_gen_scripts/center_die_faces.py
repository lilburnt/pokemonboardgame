import os
from PIL import Image

# Define the path to the directory containing the die face images
die_faces_dir = '/Users/conniesun/Documents/pokemon_game/die_faces/'

# Check if the directory exists, if not, create it and move the example file into it
# if not os.path.exists(die_faces_dir):
#     os.makedirs(die_faces_dir)
#     # Move the example file to the die_faces directory
#     os.rename('/Users/conniesun/Documents/pokemon_game/die_face_1.png', f'{die_faces_dir}die_face_1.png')

# Function to trim and make transparency outside of the die face
def process_image(image_path):
    # Load the image
    img = Image.open(image_path)
    
    # Convert to RGBA if necessary to ensure there's an alpha channel
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # Make everything outside the die face transparent
    datas = img.getdata()
    new_data = []
    for item in datas:
        # Change all white (also shades of whites) pixels to transparent
        if item[0] > 150 and item[1] > 150 and item[2] > 150:  # assuming die face is not pure white
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append((0, 0, 0, 255))

    # Update image data
    img.putdata(new_data)
    
    # Get the bounding box
    bbox = img.getbbox()
    
    # Crop the image
    cropped_img = img.crop(bbox)

    # Create a new square image with a transparent background
    square_size = max(cropped_img.size)
    square_img = Image.new('RGBA', (square_size, square_size), (0, 0, 0, 0))
    
    # Paste the cropped image onto the square image, centered
    square_img.paste(cropped_img, ((square_size - cropped_img.size[0]) // 2, 
                                   (square_size - cropped_img.size[1]) // 2), cropped_img)
    
    return square_img

# List to store the file paths of the processed images
processed_file_paths = []

# Loop through all the files in the folder and process them
for file_name in os.listdir(die_faces_dir):
    if file_name.endswith('.png'):
        # Full path to the image file
        file_path = os.path.join(die_faces_dir, file_name)
        
        # Process the image
        processed_img = process_image(file_path)
        
        # Save the processed image
        processed_img.save(file_path)
        processed_file_paths.append(file_path)

processed_file_paths
