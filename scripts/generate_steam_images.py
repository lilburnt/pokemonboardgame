import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import re

# Define the paths to the directories containing the images
backside_path = "/Users/conniesun/Documents/pokemonboardgame/artifacts/backside/edited"
pokemon_path = "/Users/conniesun/Documents/pokemonboardgame/output_folders/output"

# Define the output path of the this
final_path = "/Users/conniesun/Documents/pokemonboardgame/output_folders/final"

# Load the Excel file into a pandas DataFrame
excel_path = "/Users/conniesun/Documents/pokemonboardgame/PokemonFinal.xlsx"  # Replace with your Excel file path
pokemon_db = pd.read_excel(excel_path)

# read in the color of each pokemon
for index, row in pokemon_db.iterrows():
    color = row["Color"].strip().lower()
    pokemon_name = row["Pokemon"].strip().lower()

    # Create a regex pattern dynamically based on the pokemon_name
    pattern = rf"^{re.escape(pokemon_name)}(\W|$)"
    pokemon_files = [
        f for f in os.listdir(pokemon_path) if re.match(pattern, f.lower())
    ]
    pokemon_file = next(iter(pokemon_files), None)
    pokemon_image_path = os.path.join(pokemon_path, pokemon_file)
    pokemon_image = Image.open(pokemon_image_path).convert("RGBA")

    # Find the right color backside
    backside_image_path = os.path.join(backside_path, f"{color}.png")
    backside_image = Image.open(backside_image_path).convert("RGBA")

    # create a canvas that's 1500x1500 to fit 2x 600x600 images
    image = Image.new("RGB", (1200, 1200))

    # paste the appropriate backside image
    image.paste(backside_image, (20, 26), backside_image)

    # paste the pokemon image
    image.paste(pokemon_image, (580, 578), pokemon_image)

    output_image_path = f"{final_path}/{pokemon_name}.png"
    image.save(output_image_path, "PNG")
