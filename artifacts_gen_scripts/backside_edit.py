from PIL import Image

# Load the image
img = Image.open('/Users/conniesun/Documents/pokemon_game/backside/green.png')

# Convert the image to RGBA (if it's not already in that mode)
img = img.convert("RGBA")

# Get data of the image
datas = img.getdata()

# Create a new data list
newData = []

# Define the color to make transparent
# You might need to adjust the tolerance depending on the image
tolerance = 5

# Process the pixels
for item in datas:
    # Change all pixels that are completely black to transparent
    if item[0] <= tolerance and item[1] <= tolerance and item[2] <= tolerance:
        # Setting the alpha band to 0 makes that pixel transparent
        newData.append((255, 255, 255, 0))
    else:
        newData.append(item)

# Update image data
img.putdata(newData)

# Save the new image
img.save('/Users/conniesun/Documents/pokemon_game/backside/edited/green.png')
