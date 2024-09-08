from PIL import Image

# Reload the original blue button image with alpha channel
blue_button_path = '/Users/conniesun/Documents/pokemon_game/evolution/blue.png'
blue_button = Image.open(blue_button_path).convert('RGBA')

def color_shift(image, target_color):
    # Split into separate channels with alpha channel
    r, g, b, a = image.split()

    # Apply the color shift to the respective channels
    if target_color == "green":
        # Swap blue and red channels to make it green-ish
        result = Image.merge('RGBA', (g, b, r, a))
    elif target_color == "red":
        # Enhance the red channel
        enhanced_r = r.point(lambda i: i * 1.5 if i * 1.5 <= 255 else 255)
        reduced_g = g.point(lambda i: i * 0.7 if i * 0.7 >= 0 else 0)
        reduced_b = b.point(lambda i: i * 1.5 if i * 1.5  <= 255 else 255)
        result = Image.merge('RGBA', (reduced_b, reduced_g, enhanced_r, a))
    else:
        result = image  # No change if the color is not recognized

    return result

# Apply the color shift while maintaining the alpha channel for transparency
green_button = color_shift(blue_button, "green")
red_button = color_shift(blue_button, "red")

# Save the new images with transparent background
green_button_path = '/Users/conniesun/Documents/pokemon_game/evolution/green.png'
red_button_path = '/Users/conniesun/Documents/pokemon_game/evolution/red.png'
green_button.save(green_button_path)
red_button.save(red_button_path)

# Provide the paths to the saved files
green_button_path, red_button_path
