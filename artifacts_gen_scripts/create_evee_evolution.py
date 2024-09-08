from PIL import Image

# Load the images
vaporeon_path = '/Users/conniesun/Documents/pokemon_game/pokemon_resized/134 Vaporeon.png'
jolteon_path = '/Users/conniesun/Documents/pokemon_game/pokemon_resized/135 Jolteon.png'
flareon_path = '/Users/conniesun/Documents/pokemon_game/pokemon_resized/136 Flareon.png'

vaporeon = Image.open(vaporeon_path)
jolteon = Image.open(jolteon_path)
flareon = Image.open(flareon_path)

# Get the largest width and height to create a canvas
new_width = int(vaporeon.width * 2.0)
new_height = int(vaporeon.height * 2.0)

# Create a new image with a transparent background
canvas = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))

# Calculate the x offset for each image to be centered
vaporeon_x_offset = (new_width - vaporeon.width) / 2
jolteon_x_offset = vaporeon_x_offset - 100
flareon_x_offset = vaporeon_x_offset + 100

# Calculate the y offset for each image to be staggered
vaporeon_y_offset = 0
jolteon_y_offset = 200
flareon_y_offset = 200

# Paste the images onto the canvas
canvas.paste(vaporeon, (int(vaporeon_x_offset), int(vaporeon_y_offset)), vaporeon)
canvas.paste(jolteon, (int(jolteon_x_offset), int(jolteon_y_offset)), jolteon)
canvas.paste(flareon, (int(flareon_x_offset), int(flareon_y_offset)), flareon)

# Save the result
result_path = '/Users/conniesun/Documents/pokemon_game/pokemons/000 VaJoFl.png'
canvas.save(result_path)