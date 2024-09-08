from PIL import Image
import math
import os

# Constants for A4 paper and image sizes (in inches)
A4_WIDTH_INCHES = 8.5
A4_HEIGHT_INCHES = 11
MARGIN_INCHES = 0.5
IMAGE_DIAMETER_INCHES = 1.28

# Constants for A4 paper and image sizes (in pixels, assuming 300 dpi)
DPI = 600
A4_WIDTH = int((A4_WIDTH_INCHES - 2 * MARGIN_INCHES) * DPI)
A4_HEIGHT = int((A4_HEIGHT_INCHES - 2 * MARGIN_INCHES) * DPI)
MARGIN_PIXEL = int(MARGIN_INCHES * DPI)
IMAGE_SIZE = int(IMAGE_DIAMETER_INCHES * DPI)
BUFFER_PIXEL = int(30)

# Calculate how many images fit horizontally and vertically (without overlapping)
images_across = A4_WIDTH // (IMAGE_SIZE + BUFFER_PIXEL)
images_down = A4_HEIGHT // (IMAGE_SIZE + BUFFER_PIXEL) - 1

# Path to the directory containing images (replace with your actual folder path)
image_folder_path = '/Users/conniesun/Documents/pokemon_game/backside/edited/'

# List all the image files in the directory
image_files = [f for f in os.listdir(image_folder_path) if f.endswith('.png')]

# Calculate total number of pages needed
total_images = len(image_files)
images_per_page = images_across * images_down
total_pages = math.ceil(total_images / images_per_page)


from collections import defaultdict

# List of image filenames and the quantities we want to print
image_quantities = {
    'blue.png': 40,
    'green.png': 40,
    'pink.png': 40,
    'red.png': 40,
    'yellow.png': 10
}

# This dictionary will hold the filenames in the correct quantities
image_files = []

# Populate the image_files list
for filename, quantity in image_quantities.items():
    image_files.extend([filename] * quantity)

# Total number of images to be printed
total_images = len(image_files)

# Create a function to create pages with the images
def create_pages_with_images(image_files, images_per_page):
    # Stores the paths to the created pages
    created_pages = []
    
    # While there are still images left to place, create new pages
    current_image_index = 0
    page_number = 0
    while current_image_index < total_images:
        # Create a blank A4 page with a white background
        page = Image.new('RGB', (A4_WIDTH, A4_HEIGHT), 'white')
        
        # Place images on the page until we run out or the page is full
        for _ in range(images_per_page):
            if current_image_index >= total_images:
                break  # No more images to place
            
            # Calculate the position on the grid
            row = _ // images_across
            col = _ % images_across
            x = col * (IMAGE_SIZE + BUFFER_PIXEL) + MARGIN_PIXEL
            y = row * (IMAGE_SIZE + BUFFER_PIXEL) + MARGIN_PIXEL
            
            # Get the path to the current image
            image_path = os.path.join(image_folder_path, image_files[current_image_index])
            current_image_index += 1
            
            # Open the image and process it
            image = Image.open(image_path).convert("RGBA")
            
            # If there is transparency, we composite the image on a white background
            if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
                background = Image.new('RGBA', image.size, (255, 255, 255))
                image = Image.alpha_composite(background, image)
                
            # Resize the image
            image = image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.LANCZOS)
            # Convert to RGB
            image = image.convert('RGB')
            
            # Place the image on the page
            page.paste(image, (x, y))
        
        # Save the page to a file
        output_path = os.path.join('/Users/conniesun/Documents/pokemon_game/print/back', f'print_page_{page_number + 1}.png')
        page.save(output_path)
        created_pages.append(output_path)
        
        # Increment the page number
        page_number += 1
    
    return created_pages

# Use the function to create the pages
created_pages = create_pages_with_images(image_files, images_per_page)

created_pages
