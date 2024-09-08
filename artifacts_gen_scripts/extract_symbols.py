from PIL import Image

# Load the image
image_path = 'pokemon_types_symbols.png'
types_image = Image.open(image_path)

# Size of the image
img_width, img_height = types_image.size

# Assuming the symbols are evenly distributed in a 6x3 grid
# Calculate the size of each symbol
grid_x = 6
grid_y = 3
symbol_width = img_width // grid_x
symbol_height = img_height // grid_y

# List to store the file paths of the individual images
file_paths = []

# Loop over the grid and extract each symbol
for i in range(grid_y):
    for j in range(grid_x):
        # Define the coordinates of the rectangle to crop
        left = j * symbol_width
        top = i * symbol_height
        right = (j + 1) * symbol_width
        bottom = (i + 1) * symbol_height
        
        # Crop the symbol out of the image
        symbol = types_image.crop((left, top, right, bottom))
        
        # Convert to RGBA if necessary to ensure there's an alpha channel
        if symbol.mode != 'RGBA':
            symbol = symbol.convert('RGBA')
        
        # Create a new image with an alpha channel (transparent background)
        alpha_image = Image.new('RGBA', (symbol_width, symbol_height), (0, 0, 0, 0))
        
        # Paste the cropped symbol onto the alpha image
        alpha_image.paste(symbol, (0, 0), symbol)
        
        # Save the individual symbol
        file_name = f'/Users/conniesun/Documents/pokemon_game/symbols/pokemon_type_{i*grid_x + j}.png'
        alpha_image.save(file_name)
        file_paths.append(file_name)