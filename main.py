# Author: Filipe Chagas Ferraz
# Description: Linear Regression program
# Programming Language: Python 2
# Email: filipe.ferraz0@gmail.com
# Github account: github.com/FilipeChagasDev
# License: MIT License 

import numpy as np 
import matplotlib.pyplot as plt
import math
import random as rand
import os.path
from os import path

# function that loads the text file and turns it into a list of tuples
def load_samples (path):
    samples_file = open(path, "r")
    samples_text = "[" + samples_file.read() + "]"
    return eval(samples_text)

# square error derivative in function of angular coefficient
def SE_angular_coeff_diff (angular_coeff,linear_coeff,sample_x,sample_y):
    # SE = ( a * x + b - y)^2
    # dSE/da = 2*x*(a*x + b - y)
    # where:
    #   a = angular_coeff
    #   b = linear_coeff
    #   x = sample_x
    #   y = sample_y

    return 2 * sample_x * ( angular_coeff * sample_x + linear_coeff - sample_y ) 

# square error derivative in function of linear coefficient
def SE_linear_coeff_diff (angular_coeff,linear_coeff,sample_x,sample_y):
    # SE = ( a * x + b - y)^2
    # dSE/db = 2*(a*x + b - y)
    # where:
    #   a = angular_coeff
    #   b = linear_coeff
    #   x = sample_x
    #   y = sample_y

    return 2 * ( angular_coeff * sample_x + linear_coeff - sample_y ) 

# mean square error derivative in function of angular coefficient
def MSE_angular_coef_diff (angular_coeff, linear_coeff, samples):
    # MSE = 1/N * SE_1 + SE_2 + ... + SE_N
    # dMSE/da = 1/N * dSE_1/da * dSE_2/da + ... + dSE_N/da
    # where:
    #   dSE/da = SE_angular_coeff_diff(angular_coeff, linear_coeff, x, y)
    summation = 0
    for sample in samples:
        summation += SE_angular_coeff_diff(angular_coeff, linear_coeff, sample[0], sample[1])

    return summation/samples.shape[0] 

# mean square error derivative in function of linear coefficient
def MSE_linear_coef_diff (angular_coeff, linear_coeff, samples):
    # MSE = 1/N * SE_1 + SE_2 + ... + SE_N
    # dMSE/db = 1/N * dSE_1/db * dSE_2/db + ... + dSE_N/db
    # where:
    #   dSE/db = SE_angular_coeff_diff(angular_coeff, linear_coeff, x, y)
    summation = 0
    for sample in samples:
        summation += SE_linear_coeff_diff(angular_coeff, linear_coeff, sample[0], sample[1])
    
    return summation/samples.shape[0] 

# function that returns true if v1 is close to v2 (within tolerance range)
def approximately (val1, val2, tolerance):
    return (val1 > val2 - tolerance ) and (val1 < val2 + tolerance)

# Gradient descent function. It returns the (angular_coeff, linear_coeff) tuple
def gradient_descent (samples, ratio, tolerance):
    current_angular_coeff = rand.random()*10
    current_linear_coeff = rand.random()*10

    while True:
        dMSE_over_da = MSE_angular_coef_diff(current_angular_coeff,current_linear_coeff,samples)
        dMSE_over_db = MSE_linear_coef_diff(current_angular_coeff,current_linear_coeff, samples)    
        
        current_angular_coeff -= dMSE_over_da / ratio
        current_linear_coeff -=  dMSE_over_db / ratio

        if math.isnan(dMSE_over_da) or math.isnan(dMSE_over_db):
            raise Exception("Overflow problem in the gradient_descent iteration. Try a larger ratio.")

        if approximately(dMSE_over_da, 0, tolerance) and approximately(dMSE_over_db, 0, tolerance):
            return (current_angular_coeff, current_linear_coeff)

def main():
    samples_path = ""
    while True:
        samples_path = raw_input("enter the file path where the samples are (\"default\" or \"\" for testing): ")
        
        if samples_path in ["", "default"]:
            samples_path = "samples.txt"
            break
        elif path.exists(samples_path):
            break
        else:
            print("Invalid file path. Try again...")

    samples = np.array(load_samples(samples_path))

    ratio = float("nan")
    while True:
        ratio = float(raw_input("enter the gradient descent ratio (recommended 100): "))
        if ratio < 100:
            print("The ratio value cannot be less than 100. Try again...")
        else:
            break

    
    tolerance = float("nan")
    while True:
        tolerance = float(raw_input("enter the gradient descent tolerance (recommended 0.01): "))
        if tolerance >= 1:
            print("The tolerance most be less than 1. Try again...")
        else:
            break

    print("starting iteration...")

    (angular_coeff, linear_coeff) = gradient_descent(samples, ratio, tolerance)
    
    print("Regression successfully completed")
    print("f(x) = ax + b, where:")
    print("a = " + str(angular_coeff))
    print("b = " + str(linear_coeff))

    np_linear_func = np.vectorize(lambda x: angular_coeff * x + linear_coeff) 

    plt.plot(samples[:,0],samples[:,1],"ro",
            samples[:,0],np_linear_func(samples[:,0]))

    plt.show()

main()