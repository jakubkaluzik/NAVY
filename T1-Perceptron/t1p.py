import numpy as np
from matplotlib import pyplot as plt

def f(x):
    return 3 * x + 2

def generate_points(count, x_bounds, y_bounds):
    x_points = np.random.uniform(low=x_bounds[0], high=x_bounds[1], size=count)
    y_points = np.random.uniform(low=y_bounds[0], high=y_bounds[1], size=count)
    return list(zip(x_points, y_points))

def signum(x):
    return np.where(x > 0, 1, np.where(x < 0, -1, 0))

def perceptron_train(input, classification, iterations=200, bias=0.5, learning_rate=0.1):
    # Random starting weights for the perceptron
    weights = np.random.uniform(low=-1.0, high=1.0, size=(2,))

    for _ in range(iterations):
        for i in range(len(input)):
            a, b = input[i]
            cl = classification[i]
            # Predict the classification of the point
            predict = signum(a * weights[0] + b * weights[1] + bias)
            error = cl - predict
            # Update weights and bias based on the error
            weights[0] += error * a * learning_rate
            weights[1] += error * b * learning_rate
            bias += error * learning_rate
    
    # Return the classification of the points
    result = [signum(a * weights[0] + b * weights[1] + bias) for (a, b) in input]
    return result

def perceptron_test(points, per_classification):
    count = len(points)
    # 1 if point is above the line, -1 if below, 0 if on the line
    classification = [signum(y - f(x)) for x, y in points]
    # Check if the classification is correct
    for i in range(count):
        x, y = points[i]
        correct = classification[i] == per_classification[i]
        status = "correct" if correct else "incorrect"
        print(f"[{x}, {y}] -> {status}")
            

def show(line, points, classification):

    fig, ax = plt.subplots(figsize=(8, 6))

    # uniziping line
    x_line, y_line = zip(*line)

    ax.plot(x_line, y_line, label='y = 3x + 2')

    # Scatter points based on classification red=above=1, blue=below=-1, yellow=on=0
    for (x, y), cl in zip(points, classification):
        color = 'red' if cl == 1 else 'blue' if cl == -1 else 'yellow'
        ax.scatter(x, y, color=color)

    # Description of the plot
    ax.set_title('Perceptron')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.legend()

    # Position axis to the center
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')
    
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    plt.show()

# Bounds x for line and points
x_bounds = [-10, 10]
# Bounds y for points
y_bounds = [-20, 20]
# Generate line
x_line = np.linspace(x_bounds[0], x_bounds[1], 50)
y_line = f(x_line)
line = list(zip(x_line, y_line))

# Generate points
points = generate_points(100, x_bounds, y_bounds)

# 1 if point is above the line, -1 if below, 0 if on the line
classification = [signum(y - f(x)) for x, y in points]

per_classification = perceptron_train(points,classification)

perceptron_test(points, per_classification)

show(line, points, per_classification)