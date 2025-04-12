# IMPORTANT !!!
# To go to the next animation, close the window of the current animation.
# It will start the next one.
import numpy as np

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

def render_anim(
    x_data: list[np.array],
    y_data: list[np.array],
    z_data: list[np.array],
    model_name: str,
):
    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.set_title(f"{model_name}")
    scat = ax.scatter(x_data[0], y_data[0], z_data[0], c="black")

    def update_frame(i):
        scat._offsets3d = (x_data[i], y_data[i], z_data[i])

    animation = FuncAnimation(
        fig,
        update_frame,
        frames=len(x_data),
        interval=500,
        repeat=False,
    )
    plt.show()

# Generates random points within the specified bounds
def generate_points(bounds, n_points):

    x_data = np.random.uniform(bounds['x'][0], bounds['x'][1], n_points)
    y_data = np.random.uniform(bounds['y'][0], bounds['y'][1], n_points)
    z_data = np.random.uniform(bounds['z'][0], bounds['z'][1], n_points)

    return [x_data], [y_data], [z_data]

# loads a model data from file
def load_model(filename):
    model = np.loadtxt(filename)
    transformations = []
    for row in model:
        A = row[:9].reshape((3, 3))
        t = row[9:]
        transformations.append((A, t))
    return transformations

def iteration(current_x, current_y, current_z, transformations, n_points, bounds):
    # Initialize arrays to hold transformed points
    transformed_x = np.zeros(n_points)
    transformed_y = np.zeros(n_points)
    transformed_z = np.zeros(n_points)

    for i in range(n_points):
        # Randomly select a transformation from the list
        A, t = transformations[np.random.randint(len(transformations))]

        # Create a point vector from the current point
        point = np.array([current_x[i], current_y[i], current_z[i]])

        # Apply the transformation
        transformed_point = A @ point + t

        # Clip the transformed point to the specified bounds
        transformed_x[i] = np.clip(transformed_point[0], bounds['x'][0], bounds['x'][1])
        transformed_y[i] = np.clip(transformed_point[1], bounds['y'][0], bounds['y'][1])
        transformed_z[i] = np.clip(transformed_point[2], bounds['z'][0], bounds['z'][1])

    return transformed_x, transformed_y, transformed_z

def fern(x_data, y_data, z_data, transformations, n_points, iterations, bounds):
    for _ in range(iterations):
        # Apply the transformations to the last set of points
        transformed_x, transformed_y, transformed_z = iteration(
            x_data[-1], y_data[-1], z_data[-1], transformations, n_points, bounds
        )
        # appends the transformed points to history
        x_data.append(transformed_x)
        y_data.append(transformed_y)
        z_data.append(transformed_z)

    return x_data, y_data, z_data

def process_model(model_filename, bounds, npoints, iterations):
    x_data, y_data, z_data = generate_points(bounds, npoints)
    transformations = load_model(model_filename)
    x_data, y_data, z_data = fern(x_data, y_data, z_data, transformations, npoints, iterations=iterations, bounds=bounds)
    model_name = model_filename.split(".")[0]
    render_anim(x_data, y_data, z_data, model_name)

# Number of points to generate
npoints = 200

# Number of iterations to perform
iterations = 10

# Bounds of plot and points
bounds = {
    'x': (-1, 1),
    'y': (0, 5),
    'z': (0, 1)
}

models = ["model1.txt", "model2.txt"]

for model in models:
    process_model(model, bounds, npoints, iterations)
