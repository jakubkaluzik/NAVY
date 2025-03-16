import numpy as np
from matplotlib import pyplot as plt

# XOR function
def f(x1, x2):
    return x1 ^ x2

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivative of sigmoid
def sigmoid_(x):
    return x * (1 - x)

def snn_train(inputs, classification, iterations=5000, learning_rate=0.1):
    inputs = np.array(inputs)
    classification = np.array(classification).reshape(-1, 1)

    # Random starting weights for hidden layer
    weights_H = np.random.uniform(-1.0, 1.0, (2, 2))
    # Random starting weights for output layer
    weights_O = np.random.uniform(-1.0, 1.0, (2, 1))

    # Random starting biases for hidden layer
    bias_H = np.random.uniform(low=-1.0, high=1.0, size=(1, 2))
    # Random starting bias for output layer
    bias_O = np.random.uniform(low=-1.0, high=1.0, size=(1, 1))

    snn_before(weights_O, bias_O, weights_H, bias_H)

    for _ in range(iterations):

        # output of hidden layers
        out_H = sigmoid(np.dot(inputs, weights_H) + bias_H)

        # output of output layer
        out_O = sigmoid(np.dot(out_H, weights_O) + bias_O)

        # error calculation
        error = classification - out_O

        # calculate delta for output and hidden layers
        delta_O = error * sigmoid_(out_O)
        delta_H = delta_O.dot(weights_O.T) * sigmoid_(out_H)

        # Update weights and bias based on delta for output and hidden layers
        weights_O += out_H.T.dot(delta_O) * learning_rate
        bias_O += np.sum(delta_O, axis=0, keepdims=True) * learning_rate
        weights_H += inputs.T.dot(delta_H) * learning_rate
        bias_H += np.sum(delta_H, axis=0, keepdims=True) * learning_rate

    snn_after(weights_O, bias_O, weights_H, bias_H)

    snn_testing(out_O, classification)

    return

def snn_before(weights_O, bias_O, weights_H, bias_H):
    print("----------------------------------------")
    print("Before training...")
    print("----------------------------------------")
    print(f"Weights hidden layer: 1: {weights_H[0].tolist()}")
    print(f"Weights hidden layer: 2: {weights_H[1].tolist()}")
    print(f"Weights output layer: {weights_O.T.tolist()[0]}")
    print(f"Bias hidden layer 1: {bias_H[0, 0]}")
    print(f"Bias hidden layer 2: {bias_H[0, 1]}")
    print(f"Bias output layer: {bias_O[0, 0]}")
    print("----------------------------------------")
    print("Training...")

def snn_after(weights_O, bias_O, weights_H, bias_H):
    print("----------------------------------------")
    print("After training...")
    print("----------------------------------------")
    print(f"Weights hidden layer: 1: {weights_H[0].tolist()}")
    print(f"Weights hidden layer: 2: {weights_H[1].tolist()}")
    print(f"Weights output layer: {weights_O.T.tolist()[0]}")
    print(f"Bias hidden layer 1: {bias_H[0, 0]}")
    print(f"Bias hidden layer 2: {bias_H[0, 1]}")
    print(f"Bias output layer: {bias_O[0, 0]}")
    print("----------------------------------------")
    print("Testing...")

def snn_testing(out_O, classification):
    print("----------------------------------------")
    print("Testing results...")
    print("----------------------------------------")
    for i in range(len(out_O)):
        print(f"Input: {inputs[i]}, Predicted: {out_O[i][0]}, Expected: {classification[i]}")
    print("----------------------------------------")
   

inputs = [(0, 0), (0, 1), (1, 0), (1, 1)]
# XOR [0, 1, 1, 0]
classification = [f(x1, x2) for x1, x2 in inputs]

snn_train(inputs, classification)

