import cv2
import numpy as np

def create_metallic_ring(color, size=(600, 600), ring_radius=302, ring_width=80, border_thickness=0):
    # Create a blank RGBA image (last channel for transparency)
    image = np.zeros((size[1], size[0], 4), dtype=np.uint8)

    # Create a circular mask for the outer ring
    mask = np.zeros((size[1], size[0]), dtype=np.uint8)
    cv2.circle(mask, (size[1]//2, size[0]//2), ring_radius, 255, -1)

    # Create a mask for the inner circle and subtract it from the outer ring mask
    cv2.circle(mask, (size[1]//2, size[0]//2), ring_radius - ring_width, 0, -1)

    # Apply the color to the ring and full opacity
    image[mask > 0] = (*color, 255)

    # Apply a radial gradient for the transparency from the inner edge to the center
    y, x = np.ogrid[:size[1], :size[0]]
    center = (size[0] / 2, size[1] / 2)
    distance_from_center = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    gradient = np.clip((distance_from_center - ring_radius + ring_width) / ring_width, 0.0, 1)
    alpha_mask = (mask > 0).astype(np.float32) * gradient
    image[..., 3] = (alpha_mask * 255).astype(np.uint8)

    # # Create and apply the eigengrau border around the ring
    # eigengrau_color = (22, 22, 29, 255)  # Eigengrau color with full opacity
    # border_mask = np.zeros((size[1], size[0]), dtype=np.uint8)
    # cv2.circle(border_mask, (size[1]//2, size[0]//2), ring_radius + 2, 255, -1)
    # cv2.circle(border_mask, (size[1]//2, size[0]//2), ring_radius - border_thickness, 0, -1)
    # image[border_mask > 0] = eigengrau_color

    return image

# Define colors
dark_factor = 0.75
colors = {
    'blue': (245 * dark_factor, 100 * dark_factor, 50 * dark_factor),
    'green': (120 * dark_factor, 180 * dark_factor, 30 * dark_factor),
    'yellow': (30 * dark_factor, 170 * dark_factor, 230 * dark_factor),
    'red': (50 * dark_factor, 70 * dark_factor, 200 * dark_factor),
    'pink': (200 * dark_factor, 100 * dark_factor, 200 * dark_factor)
}

# Generate and save the images
for color_name, color_value in colors.items():
    image = create_metallic_ring(color_value)
    cv2.imwrite(f'/Users/conniesun/Documents/pokemon_game/rings/metallic_ring_{color_name}.png', image)