import os
from PIL import Image
import numpy as np

def resize_pokemon_image(image_path, target_dim_h, target_dim_w):
    """
    Resizes a Pokémon image such that the non-transparent part is a specific height, maintaining aspect ratio.

    Parameters:
    image_path (str): The path to the image file.
    target_height (int): The desired height for the non-transparent part of the image.

    Returns:
    Image: The resized image with the non-transparent part at the desired height.
    """
    with Image.open(image_path) as img:
        # Convert image to numpy array
        img_np = np.array(img)

        # Find the bounds of the non-transparent part of the image
        non_transparent_rows = np.where(np.any(img_np[:, :, 3] != 0, axis=1))[0]
        non_transparent_cols = np.where(np.any(img_np[:, :, 3] != 0, axis=0))[0]

        # Crop the image to the non-transparent part
        cropped_img_np = img_np[non_transparent_rows.min():non_transparent_rows.max(),
                                non_transparent_cols.min():non_transparent_cols.max()]

        # Convert back to image
        cropped_img = Image.fromarray(cropped_img_np, 'RGBA')

        # Calculate the new width while maintaining the aspect ratio
        ratio_height =  target_dim_h / cropped_img.height
        ratio_width =  target_dim_w / cropped_img.width
        # scale to the smaller one of the 2
        scale = min(ratio_width, ratio_height)
        # Resize the cropped image
        resized_img = cropped_img.resize((int(cropped_img.width * scale), int(cropped_img.height * scale)), Image.LANCZOS)

        return resized_img

def resize_pokemon_images_in_folder(input_folder, target_height, target_width, output_folder):
    """
    Iterates through a folder, resizing each Pokémon image.

    Parameters:
    input_folder (str): Path to the folder containing images.
    target_height (int): The desired height for the non-transparent part of the image.
    output_folder (str): Path to the folder where resized images will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all .png files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith('.png'):
            image_path = os.path.join(input_folder, file_name)
            resized_img = resize_pokemon_image(image_path, target_height, target_width)
            resized_img.save(os.path.join(output_folder, file_name))
            print(f'resizing image {file_name}')

# Example usage:
resize_pokemon_images_in_folder('/Users/conniesun/Documents/pokemon_game/pokemons', 300, 375, '/Users/conniesun/Documents/pokemon_game/pokemon_resized')
