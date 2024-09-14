from PIL import Image
import math
import os

# Constants for A4 paper and image sizes (in inches)
A4_WIDTH_INCHES = 8.5
A4_HEIGHT_INCHES = 11
MARGIN_INCHES = 0.4
IMAGE_DIAMETER_INCHES = 1.3

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
image_folder_path = "/Users/conniesun/Documents/pokemonboardgame/output_folders/output/"

# List all the image files in the directory
image_files = [f for f in os.listdir(image_folder_path) if f.endswith(".png")]

# Calculate total number of pages needed
total_images = len(image_files)
images_per_page = images_across * images_down
total_pages = math.ceil(total_images / images_per_page)


# Function to create a single page with images
def create_print_page(page_number, image_files, images_per_page):
    # Create a blank A4 page with a white background
    page = Image.new("RGB", (A4_WIDTH, A4_HEIGHT), "white")

    # Calculate the starting index of the image to print on this page
    start_index = page_number * images_per_page

    # Place each image on the page
    for i in range(images_per_page):
        # Calculate the position on the grid
        row = i // images_across
        col = i % images_across
        x = col * (IMAGE_SIZE + BUFFER_PIXEL) + MARGIN_PIXEL
        y = row * (IMAGE_SIZE + BUFFER_PIXEL) + MARGIN_PIXEL

        # Check if we still have images left to print
        if start_index + i < total_images:
            image_path = os.path.join(image_folder_path, image_files[start_index + i])
            image = Image.open(image_path)

            # Check if the image has an alpha channel
            if image.mode in ("RGBA", "LA") or (
                image.mode == "P" and "transparency" in image.info
            ):
                # Create a white background
                background = Image.new("RGBA", image.size, (255, 255, 255))
                # Composite the image onto the white background
                image = Image.alpha_composite(background, image)

            # Resize the image to fit the page
            image = image.resize((IMAGE_SIZE, IMAGE_SIZE), Image.Resampling.LANCZOS)

            # Convert the image to RGB mode to paste it on the page
            image = image.convert("RGB")

            # Place the image on the page
            page.paste(image, (x, y))

    # Save the page to a file
    output_path = os.path.join(
        "/Users/conniesun/Documents/pokemonboardgame/output_folders/print/",
        f"print_page_{page_number + 1}.png",
    )
    page.save(output_path)
    return output_path


# Create and save all pages
created_pages = []
for page_number in range(total_pages):
    page_path = create_print_page(page_number, image_files, images_per_page)
    created_pages.append(page_path)

# Return a list of created pages paths
created_pages
