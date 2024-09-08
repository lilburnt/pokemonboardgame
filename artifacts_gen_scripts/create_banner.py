from PIL import Image, ImageDraw, ImageFont
import pandas as pd

def create_banner(text, banner_size=(550, 65), corner_radius=40, font_size=50):
    # Create a new image with transparent background
    banner = Image.new('RGBA', banner_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(banner)

    # Draw a rounded rectangle on the banner
    draw.rounded_rectangle([(0, 0), banner_size], corner_radius, fill=(22, 22, 29))

    # Load a font
    try:
        # Font path might need to be changed depending on where the fonts are located on your system
        font = ImageFont.truetype("PocketMonk-15ze.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text size and position
    text_width = draw.textlength(text, font=font)
    text_height = 50
    text_position = ((banner_size[0] - text_width) / 2, (banner_size[1] - text_height) / 2)

    # Draw text on the banner
    draw.text(text_position, text, font=font, fill="white")

    # Save the banner
    output_path = f'/Users/conniesun/Documents/pokemon_game/banners/{text}.png'
    banner.save(output_path)

    return output_path

xlsx_file = 'PokemonFinal.xlsx'

# Read the data into a pandas DataFrame
df = pd.read_excel(xlsx_file)

# Iterate through the 'Pokemon' column and create a banner for each
for pokemon in df['Pokemon']:
    banner_path = create_banner(pokemon)
    print(f'Banner created for {pokemon}: {banner_path}')