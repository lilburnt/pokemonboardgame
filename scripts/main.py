import os
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import re

# Load the Excel file into a pandas DataFrame
excel_path = "/Users/conniesun/Documents/pokemon_game/PokemonFinal.xlsx"  # Replace with your Excel file path
pokemon_db = pd.read_excel(excel_path)

# Define the paths to the directories containing the images
backgrounds_path = "/Users/conniesun/Documents/pokemon_game/backgrounds/cropped"
rings_path = "/Users/conniesun/Documents/pokemon_game/rings"
pokemons_path = "/Users/conniesun/Documents/pokemon_game/pokemon_resized"
banners_path = "/Users/conniesun/Documents/pokemon_game/banners"
symbols_path = "/Users/conniesun/Documents/pokemon_game/symbols"
attack_strength_path = "/Users/conniesun/Documents/pokemon_game/attack_strengths"
evolution_path = "/Users/conniesun/Documents/pokemon_game/evolution"


# Function to extract numbers from a string
def extract_numbers(s):
    return re.findall(r"\b\d+\b", str(s))


# Function to overlay images
def overlay_images(
    background,
    ring,
    pokemon,
    banner,
    symbol,
    symbol2,
    attack,
    evolution,
    next_pokemon,
    output_path,
):
    # Open the background and ring images
    bg_image = Image.open(background).convert("RGBA")
    ring_image = Image.open(ring).convert("RGBA")

    # Overlay the ring onto the background
    composite = Image.alpha_composite(bg_image, ring_image)

    # Open the pokemon image, resize it and define its position
    pokemon_image = Image.open(pokemon).convert("RGBA")
    # pokemon_image = pokemon_image.resize((300, 300))
    # Calculate position: centered in X, 2/3 up in Y
    x_pokemon = (composite.size[0] - pokemon_image.size[0]) // 2
    # y_pokemon = int(float(composite.size[1] - pokemon_image.size[1]) * 0.175)
    y_pokemon = 190 - int(pokemon_image.size[1] / 2)

    # Overlay the next evolution of the pokemon, if possible
    if next_pokemon != "none":
        next_pokemon_image = Image.open(next_pokemon).convert("RGBA")
        scale = min(125 / next_pokemon_image.width, 125 / next_pokemon_image.height)
        next_pokemon_image = next_pokemon_image.resize(
            (
                int(next_pokemon_image.width * scale),
                int(next_pokemon_image.height * scale),
            )
        )
        x_next_pokemon = 450
        y_next_pokemon = 220
        # Overlay the next pokemon image onto the composite image
        composite.paste(
            next_pokemon_image, (x_next_pokemon, y_next_pokemon), next_pokemon_image
        )

    # Overlay the pokemon image onto the composite image
    composite.paste(pokemon_image, (x_pokemon, y_pokemon), pokemon_image)

    # Overlay the banner
    banner_image = Image.open(banner).convert("RGBA")
    x_banner = (composite.size[0] - banner_image.size[0]) // 2
    y_banner = int(float(composite.size[1] - banner_image.size[1]) * 0.62)
    composite.paste(banner_image, (x_banner, y_banner), banner_image)

    # Overaly the secondary symbols first (on top), if any
    if symbol2 != "none":
        symbol_image = Image.open(symbol2).convert("RGBA")
        symbol_image = symbol_image.resize((45, 45))
        x_symbol = 75
        composite.paste(symbol_image, (x_symbol, y_banner + 10), symbol_image)

    # Overlay the symbols
    symbol_image = Image.open(symbol).convert("RGBA")
    symbol_image = symbol_image.resize((55, 55))
    x_symbol = 30
    composite.paste(symbol_image, (x_symbol, y_banner + 5), symbol_image)

    # Overlay the attack strength
    attack_image = Image.open(attack).convert("RGBA")
    target_height = 100
    scale = target_height / attack_image.height
    attack_image = attack_image.resize(
        (int(attack_image.width * scale), int(attack_image.height * scale))
    )
    if "final" in evolution:
        x_attack = int(500 - attack_image.width / 2)
    else:
        x_attack = 50
    y_attack = int(float(composite.size[1] - banner_image.size[1]) * 0.42)
    composite.paste(attack_image, (x_attack, y_attack), attack_image)

    # Overlay the evolution
    evolution_image = Image.open(evolution).convert("RGBA")
    evolution_image = evolution_image.resize(
        (int(evolution_image.width * 0.7), int(evolution_image.height * 0.7))
    )
    x_evolution = 470
    y_evolution = int(float(composite.size[1] - evolution_image.size[1]) * 0.61)

    if (
        ("blue" in evolution)
        or ("green" in evolution)
        or ("red" in evolution)
        or ("stone" in evolution)
    ):
        composite.paste(
            evolution_image, (x_evolution + 37, y_evolution + 3), evolution_image
        )
    elif "xp" in evolution:
        composite.paste(evolution_image, (x_evolution, y_evolution), evolution_image)
    else:
        print(pokemon + " does not have a valid evolution")
    # Save the final composite image
    composite.save(output_path, "PNG")


def create_dice_roll_image(rolls, image_folder="die_faces", spacing=20):
    # List to store individual die face images
    images = []

    # Load the die face images based on the rolls
    for roll in rolls:
        image_path = os.path.join(image_folder, f"die_face_{roll}.png")
        try:
            die_image = Image.open(image_path)
            images.append(die_image)
        except FileNotFoundError:
            print(f"No image found for roll {roll}")

    # Calculate the width and height of the final image
    width = sum(image.width for image in images) + spacing * (len(images) - 1)
    height = max(image.height for image in images)

    # Create a new image with the calculated width and height
    composite_image = Image.new("RGBA", (width, height))

    # Paste each die face image onto the composite image
    current_x = 0
    for image in images:
        composite_image.paste(image, (current_x, 0))
        current_x += image.width + spacing

    return composite_image


def create_composite_image(numbers, image_folder):
    images = [Image.open(f"{image_folder}/die_faces_{n}.png") for n in numbers if n]
    if not images:
        return Image.new("RGBA", (100, 100), (0, 0, 0, 0))  # Empty image for empty rows

    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    composite_image = Image.new("RGBA", (total_width, max_height), (0, 0, 0, 0))

    x_offset = 0
    for img in images:
        composite_image.paste(img, (x_offset, 0))
        x_offset += img.size[0]

    return composite_image


def process_excel_file(file_path, image_folder, output_folder):
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        numbers = (
            row["How to Catch"].split(",") if row["How to Catch"] else []
        )  # Replace 'Column Name' with your column name
        composite_image = create_composite_image(numbers, image_folder)
        composite_image.save(f"{output_folder}/composite_row_{index}.png")


# Iterate over the Pokémon database and create the composite images
for index, row in pokemon_db.iterrows():
    # Get the background, ring, and pokemon images
    type_1 = row["Type 1"].strip().lower()
    type_2 = (
        row["Type 2"].strip().lower() if (isinstance(row["Type 2"], str)) else "none"
    )
    color = row["Color"].strip().lower()
    pokemon_name = row["Pokemon"].strip().lower()
    attack_strength = str(int(row["Attack \nStrength"]))
    evolution_in = row["How to Evolve"]
    evolution_stage = row["Evolution \nStage"]
    next_pokemon = row["Next Evolution"].strip().lower()
    catch_roll = row["How to Catch"] if isinstance(row["How to Catch"], str) else "none"
    special_ability_1 = (
        row["Special \nAbility 1"]
        if isinstance(row["Special \nAbility 1"], str)
        else "none"
    )
    special_ability_2 = (
        row["Special \nAbility 2"]
        if isinstance(row["Special \nAbility 2"], str)
        else "none"
    )

    # if pokemon_name != "pidgeotto":
    #     continue
    # Get a list of all background files that match the "Type 1" and pick a random one
    background_files = [
        f for f in os.listdir(backgrounds_path) if f.lower().startswith(f"{type_1}_")
    ]
    # background_file = random.choice(background_files)
    for backcount in range(5):
        background_file = background_files[backcount]
        background_image_path = os.path.join(backgrounds_path, background_file)

        # Get the ring image path
        ring_image_path = os.path.join(rings_path, f"metallic_ring_{color}.png")

        # Create a regex pattern dynamically based on the pokemon_name
        pattern = rf"^{re.escape(pokemon_name)}(\W|$)"
        pokemon_files = [
            f for f in os.listdir(pokemons_path) if re.match(pattern, f[4:].lower())
        ]

        # Get the pokemon image path, ignoring the first 4 characters of the file name
        # pokemon_files = [f for f in os.listdir(pokemons_path) if f[4:].lower().startswith(pokemon_name)]
        pokemon_file = next(iter(pokemon_files), None)
        pokemon_image_path = os.path.join(pokemons_path, pokemon_file)

        # Get the pokemon banner path
        # banner_files = [f for f in os.listdir(banners_path) if f.lower() == (pokemon_name)]
        banner_files = [
            f for f in os.listdir(banners_path) if re.match(pattern, f.lower())
        ]
        banner_file = next(iter(banner_files), None)
        banner_image_path = os.path.join(banners_path, banner_file)

        # Get the pokemon symbols path
        symbols_files = [
            f for f in os.listdir(symbols_path) if f.lower().startswith(f"{type_1}")
        ]
        symbols_file = next(iter(symbols_files), None)
        symbols_image_path = os.path.join(symbols_path, symbols_file)

        # Get the pokemon's secondary symbols path
        second_symbols_image_path = "none"
        if type_2 != "none":
            symbols_files = [
                f for f in os.listdir(symbols_path) if f.lower().startswith(f"{type_2}")
            ]
            symbols_file = next(iter(symbols_files), None)
            second_symbols_image_path = os.path.join(symbols_path, symbols_file)

        # Get the attack strength
        as_files = [
            f
            for f in os.listdir(attack_strength_path)
            if f[3:].lower().startswith(f"{attack_strength}")
        ]
        as_file = next(iter(as_files), None)
        as_image_path = os.path.join(attack_strength_path, as_file)

        # Get the evolution path
        evolution_steps = ["Green", "Red", "Blue", "Cinnabar", "Fuchsia", "Safari"]
        evolution_steps_map = {
            "Green": "green",
            "Red": "red",
            "Blue": "blue",
            "Cinnabar": "cinnabar",
            "Fuchsia": "fuchsia",
            "Safari": "safari",
            "Evolution Stone": "evolution_stone",
        }

        evolution = ""
        if not isinstance(evolution_in, str):
            evolution = "final"
        elif evolution_in in evolution_steps_map:
            evolution = evolution_steps_map[evolution_in]
        else:
            number = re.findall(r"\d+", evolution_in)
            evolution = str(int(number[0]))

        # Get the evolution path
        evolution_files = [
            f
            for f in os.listdir(evolution_path)
            if f.lower().startswith(f"{evolution}")
        ]
        evolution_file = next(iter(evolution_files), None)
        evolution_image_path = os.path.join(evolution_path, evolution_file)

        # Get the next evolution, if any
        next_pokemon_image_path = "none"
        if next_pokemon != "none":
            pattern = rf"^{re.escape(next_pokemon)}(\W|$)"
            next_pokemon_files = [
                f for f in os.listdir(pokemons_path) if re.match(pattern, f[4:].lower())
            ]
            next_pokemon_file = next(iter(next_pokemon_files), None)
            next_pokemon_image_path = os.path.join(pokemons_path, next_pokemon_file)

        # Define the output path for the composite image
        output_image_path = f"/Users/conniesun/Documents/pokemon_game/output/{pokemon_name}_{backcount}.png"  # Replace with your output directory path

        # Create the composite image
        if background_file and pokemon_file:
            overlay_images(
                background_image_path,
                ring_image_path,
                pokemon_image_path,
                banner_image_path,
                symbols_image_path,
                second_symbols_image_path,
                as_image_path,
                evolution_image_path,
                next_pokemon_image_path,
                output_image_path,
            )
        else:
            print(f"Image files for {pokemon_name} could not be found.")

        # Add special skills to the images
        font = ImageFont.truetype("Gill Sans Bold", 40)
        image = Image.open(output_image_path)
        image_width, image_height = image.size
        draw = ImageDraw.Draw(image)
        red_text = [
            "Freeze",
            "Constrict",
            "Burn",
            "Armored",
            "Rage",
            "Toxic",
            "Critical",
            "Recover",
            "Blitz",
            "Intimidate",
            "Quick Attack",
            "One-Hit KO",
        ]
        if (special_ability_1 != "none") and (special_ability_2 != "none"):
            # Calculate text size and position
            text_width1 = draw.textlength(special_ability_1, font=font)
            text_width2 = draw.textlength(special_ability_2, font=font)
            middle_width = draw.textlength(", ", font=font)
            total_width = text_width1 + text_width2 + middle_width

            position1 = ((image_width - total_width) / 2, 425)
            text_color = (
                (139, 0, 0)
                if any(keyword in special_ability_1 for keyword in red_text)
                else (22, 22, 29)
            )
            draw.text(position1, special_ability_1, font=font, fill=text_color)

            position2 = ((image_width - total_width) / 2 + text_width1, 425)
            draw.text(position2, ", ", font=font, fill="black")

            position3 = (
                (image_width - total_width) / 2 + text_width1 + middle_width,
                425,
            )
            text_color = (
                (139, 0, 0)
                if any(keyword in special_ability_2 for keyword in red_text)
                else (22, 22, 29)
            )
            draw.text(position3, special_ability_2, font=font, fill=text_color)
        elif special_ability_1 != "none":
            # Calculate text size and position
            text_width = draw.textlength(special_ability_1, font=font)
            position = ((image_width - text_width) / 2, 425)
            text_color = (
                (139, 0, 0)
                if any(keyword in special_ability_1 for keyword in red_text)
                else (22, 22, 29)
            )
            draw.text(position, special_ability_1, font=font, fill=text_color)

        # Add catch roll
        catch_font = ImageFont.truetype("Gill Sans Medium Italic", 40)
        if catch_roll == "none":
            # no catch roll needed
            print("no catch roll needed")
        elif ("," in catch_roll) or len(catch_roll) == 1:
            catch_numbers = [int(num.strip()) for num in catch_roll.split(",")]
            images = [
                Image.open(
                    f"/Users/conniesun/Documents/pokemon_game/die_faces/die_face_{n}.png"
                )
                for n in catch_numbers
                if n
            ]
            widths, heights = zip(*(i.size for i in images))
            total_width = sum(widths)
            max_height = max(heights)
            composite_image = Image.new("RGBA", (total_width, max_height), (0, 0, 0, 0))
            x_offset = 0
            for img in images:
                composite_image.paste(img, (x_offset, 0))
                x_offset += img.size[0]
            width, height = composite_image.size
            scale = 50 / height
            composite_image = composite_image.resize(
                (int(width * scale), int(height * scale))
            )
            new_x = int((image.width - int(width * scale)) / 2)
            image.paste(composite_image, (new_x, 480), composite_image)
        elif "," not in catch_roll:
            if "Trade" in catch_roll:
                catch_roll_text = catch_roll[6:]
                text_width = draw.textlength(catch_roll, font=catch_font)
                position = ((image_width - text_width) / 2, 480)
                draw.text(position, catch_roll, font=catch_font, fill="black")
            else:
                text_width = draw.textlength(catch_roll, font=catch_font)
                position = ((image_width - text_width) / 2, 480)
                draw.text(position, catch_roll, font=catch_font, fill="black")

        # Save or display the image
        image.save(output_image_path)
