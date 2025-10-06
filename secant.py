import numpy as np
import pandas as pd
from sympy import sympify, lambdify

def secant_method(function_str, x0, x1, epsilon=0.001, max_iter=100):
    x = sympify(function_str)
    f = lambdify(x, x, 'numpy')
    
    # Inisialisasi
    iteration = 2
    results = []
    prev_x = x0
    curr_x = x1
    prev_f = f(prev_x)
    curr_f = f(curr_x)
