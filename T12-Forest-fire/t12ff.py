# IMPORTANT !!!
# This is a simulation of an infinite forest fire model.
# On top of tree, fire and burned i added empty space.
# These empty spaces are used to plant new trees and to simulate the growth of the forest

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

def render_anim(size, p, f, density, model_name):
    forest = init_forest(size, density)

    fig, ax = plt.subplots()
    ax.set_title(model_name)
    cmap = ListedColormap(['white', 'green', 'red', 'black'])
    img = ax.imshow(forest, cmap=cmap, vmin=0, vmax=3, interpolation='nearest', origin='lower')

    def update_frame(_):
        nonlocal forest
        forest = update_forest(forest, size, p, f)
        img.set_data(forest)
        return [img]

    anim = FuncAnimation(
        fig,
        update_frame,
        interval=100,
        blit=True,
        repeat=True,
        cache_frame_data=False
    )

    plt.show()

# Function to initialize the forest with trees and fire
# empty = 0, tree = 1, fire = 2, burned = 3
def init_forest(size, density):
    empty, tree, fire = 0, 1, 2
    # Initialize the forest with trees and empty spaces
    forest = np.random.choice([empty, tree], size=(size, size), p=[1 - density, density])

    # Set a random number of trees on fire
    fire_start = np.random.choice(size * size, size // 20, replace=False)
    for idx in fire_start:
        x, y = divmod(idx, size)
        if forest[x, y] == tree:
            forest[x, y] = fire
    return forest

# Function to update the forest state
def update_forest(forest, size, p, f):
    empty, tree, fire, burned = 0, 1, 2, 3
    new_forest = forest.copy()

    for i in range(size):
        for j in range(size):
            cell = forest[i, j]
            # Randomly decide to plant a new tree if the cell is empty or burned
            if cell == empty or cell == burned:
                new_forest[i, j] = tree if np.random.rand() < p else empty
            # If the cell is a tree, check for fire spread    
            elif cell == tree:
                # Check the four neighboring cells for fire
                # If any neighbor is on fire, the tree catches fire
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < size and 0 <= nj < size and forest[ni, nj] == fire:
                        new_forest[i, j] = fire
                        break
                else:
                    # If it doesnt have fire neighbors, it may catch fire with probability f
                    if np.random.rand() < f:
                        new_forest[i, j] = fire
            elif cell == fire:
                # If the cell is on fire, it burns out
                new_forest[i, j] = burned

    return new_forest

if __name__ == "__main__":
    size = 100
    p = 0.05
    f = 0.001
    density = 0.8
    render_anim(size, p, f, density, model_name="Infinite Forest Fire Simulation")