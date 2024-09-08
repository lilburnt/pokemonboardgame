from PIL import Image

# Load the image
image_path = '/Users/conniesun/Documents/pokemon_game/die_faces.png'
dice_image = Image.open(image_path)

# Size of the image
img_width, img_height = dice_image.size

# Assuming the dice are evenly spaced in a row, calculate the width of each die face
die_width = img_width // 6

# List to store the file paths of the individual dice faces
file_paths = []

# Loop over the image and extract each die face
for i in range(6):
    # Define the coordinates of the rectangle to crop
    left = i * die_width
    top = 0
    right = (i + 1) * die_width
    bottom = img_height
    
    # Crop the die face out of the image
    die_face = dice_image.crop((left, top, right, bottom))
    
    # Save the individual die face
    file_name = f'/Users/conniesun/Documents/pokemon_game/die_faces/die_face_{i+1}.png'
    die_face.save(file_name)
    file_paths.append(file_name)