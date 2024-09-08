import pandas as pd
from PIL import Image

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
        catch_roll = row['How to Catch']
        if not isinstance(catch_roll, str):
            # no catch roll needed
            print("no catch roll needed")
        elif 'Trade:' in catch_roll:
            # test
        elif (',' in catch_roll) or isinstance(catch_roll, int):
            numbers = catch_roll.split(',') if catch_roll else []  # Replace 'Column Name' with your column name
            composite_image = create_composite_image(numbers, image_folder)
            composite_image.save(f"{output_folder}/composite_row_{index}.png")
        else:
            


# Parameters
excel_file_path = '/Users/conniesun/Documents/pokemon_game/PokemonFinal.xlsx'  # Update with your Excel file path
image_folder = '/Users/conniesun/Documents/pokemon_game/die_faces'    # Update with your images folder path
output_folder = '/Users/conniesun/Documents/pokemon_game/die_faces/temp_die'      # Update with your desired output folder path

process_excel_file(excel_file_path, image_folder, output_folder)
