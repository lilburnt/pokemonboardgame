from PIL import Image

new_size = 75

blue_button_path = '/Users/conniesun/Documents/pokemon_game/evolution/original/blue.png'
blue_button = Image.open(blue_button_path)
new_blue = blue_button.resize((new_size, new_size), Image.LANCZOS)
new_blue.save('/Users/conniesun/Documents/pokemon_game/evolution/blue.png')

green_button_path = '/Users/conniesun/Documents/pokemon_game/evolution/original/green.png'
green_button = Image.open(green_button_path)
new_green = green_button.resize((new_size, new_size), Image.LANCZOS)
new_green.save('/Users/conniesun/Documents/pokemon_game/evolution/green.png')

red_button_path = '/Users/conniesun/Documents/pokemon_game/evolution/original/red.png'
red_button = Image.open(red_button_path)
new_red = red_button.resize((new_size, new_size), Image.LANCZOS)
new_red.save('/Users/conniesun/Documents/pokemon_game/evolution/red.png')

evo_button_path = '/Users/conniesun/Documents/pokemon_game/evolution/original/evolution_stone.png'
evo_button = Image.open(evo_button_path)
new_evo = evo_button.resize((new_size, new_size), Image.LANCZOS)
new_evo.save('/Users/conniesun/Documents/pokemon_game/evolution/evolution_stone.png')