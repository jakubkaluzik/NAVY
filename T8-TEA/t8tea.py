# IMPORTANT !!!
# Use the left mouse button to zoom in and the right mouse button to zoom out.
# It might take a few seconds to zoom or zoom out because of calculating the Mandelbrot set.
import numpy as np
import matplotlib.pyplot as plt

# Paramaters for the Mandelbrot set
x0 = (-2.0, 1.0)
y0 = (-1.5, 1.5)
res = (600, 400)
max_iter = 100

def mandelbrot_set(x_range, y_range, resolution, max_iterations):
    width, height = resolution
    data = np.zeros((height, width), dtype=int)

    #For each pixel in the image
    for px in range(width):
        for py in range(height):
            x = x_range[0] + (px / width) * (x_range[1] - x_range[0])
            y = y_range[0] + (py / height) * (y_range[1] - y_range[0])

            zx = 0.0
            zy = 0.0
            iteration = 0

            while (zx * zx + zy * zy <= 4) and (iteration < max_iterations):
                xtemp = zx * zx - zy * zy + x
                zy = 2 * zx * zy + y
                zx = xtemp
                iteration += 1

            data[py, px] = iteration

    return data

def plot_mandelbrot(fig, ax, img, x_range, y_range, resolution, max_iterations):
    data = mandelbrot_set(x_range, y_range, resolution, max_iterations)
    
    if img is None:
        img = ax.imshow(data, extent=[x_range[0], x_range[1], y_range[0], y_range[1]], 
                       cmap='hot', origin='lower')
    else:
        img.set_data(data)
        img.set_extent([x_range[0], x_range[1], y_range[0], y_range[1]])
    
    ax.set_title(f"Zoom: x=[{x_range[0]:.3f}, {x_range[1]:.3f}], y=[{y_range[0]:.3f}, {y_range[1]:.3f}]")
    fig.canvas.draw_idle()
    
    return img

def on_click(event):
    global x0, y0
    # Check if the event is a mouse click and if the coordinates are valid
    # Check for left or right mouse button click
    if event.button == 1 and event.xdata is not None and event.ydata is not None:
        zoom_factor = 0.5
    elif event.button == 3 and event.xdata is not None and event.ydata is not None:
        zoom_factor = 2.0
    else:
        return

    x_center = event.xdata
    y_center = event.ydata

    #Zoom and recalibrate the x0 and y0 ranges
    x_range = (x0[1] - x0[0]) * zoom_factor
    y_range = (y0[1] - y0[0]) * zoom_factor

    x0 = (x_center - x_range / 2, x_center + x_range / 2)
    y0 = (y_center - y_range / 2, y_center + y_range / 2)

    global img
    img = plot_mandelbrot(fig, ax, img, x0, y0, res, max_iter)

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(8, 8))
    img = None
    img = plot_mandelbrot(fig, ax, img, x0, y0, res, max_iter)
    
    fig.canvas.mpl_connect("button_press_event", on_click)
    plt.show()