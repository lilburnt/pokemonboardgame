import os
from PIL import Image
import numpy as np

for file_name in os.listdir('/Users/conniesun/Documents/pokemon_game/backside/edited'):
    file_path = os.path.join('/Users/conniesun/Documents/pokemon_game/backside/edited', file_name)
    with Image.open(file_path) as img:
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
        
        # Resize the cropped image
        resized_img = cropped_img.resize((600, 600), Image.LANCZOS)
        resized_img.save(os.path.join('/Users/conniesun/Documents/pokemon_game/backside/edited2', file_name))
