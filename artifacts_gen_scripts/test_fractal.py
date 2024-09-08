import numpy as np
import matplotlib.pyplot as plt

# Function to check if a point is in the Mandelbrot set
def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    if n == max_iter:
        return max_iter
    return n + 1 - np.log(np.log2(abs(z)))

# Increase the image size for higher resolution
width, height = 1200, 1200

# Adjust plot window for more intricate details
xmin, xmax = -2, 1
ymin, ymax = -1.5, 1.5

# Generate a grid of complex numbers
x = np.linspace(xmin, xmax, width)
y = np.linspace(ymin, ymax, height)
X, Y = np.meshgrid(x, y)
Z = X + 1j * Y

# Mandelbrot calculation with a higher maximum iteration for more detail
max_iter = 500
C = np.vectorize(mandelbrot)(Z, max_iter)

# Plotting with a rainbow color map
plt.imshow(C, cmap="rainbow", extent=[xmin, xmax, ymin, ymax])
plt.colorbar()
plt.title("Mandelbrot Set in Rainbow Colors")
plt.show()
