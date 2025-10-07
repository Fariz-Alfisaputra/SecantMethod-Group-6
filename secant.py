import numpy as np
import pandas as pd
from sympy import sympify, lambdify

def secant_method(function_str, x0, x1, epsilon=0.001, max_iter=100):
    x = sympify(function_str)
    f = lambdify(x, x, 'numpy')
    
    iteration = 2 
    results = []
    prev_x = x0
    curr_x = x1
    prev_f = f(prev_x)
    curr_f = f(curr_x)
    
    while iteration <= max_iter:
        #Rumus secant
        next_x = curr_x - curr_f * (curr_x - prev_x) / (curr_f - prev_f)
        next_f = f(next_x)
        error = abs(next_x - curr_x)
        
        #Simpan hasil
        results.append({
            'n': iteration,
            'x_{n-1}': prev_x,
            'x_n': curr_x,
            'x_{n+1}': next_x,
            'f(x_{n+1})': next_f,
            'e': error
        })
        
        #Cek konvergensi
        if error < epsilon or abs(next_f) < epsilon:
            return pd.DataFrame(results), next_x
        
        #Update untuk iterasi berikutnya
        prev_x, curr_x = curr_x, next_x
        prev_f, curr_f = curr_f, next_f
        iteration += 1
    
    return pd.DataFrame(results), next_x

if __name__ == "__main__":
    func = input("Masukkan fungsi f(x) (contoh: 'x**3 - 2*x - 5'): ")
    x0 = float(input("Masukkan x0: "))
    x1 = float(input("Masukkan x1: "))
    eps = float(input("Masukkan toleransi epsilon (default 0.001): ") or 0.001)
    
    table, root = secant_method(func, x0, x1, eps)
    print("\nTabel Iterasi:")
    print(table.to_string(index=False, float_format='%.3f'))
    print(f"\nAkar aproksimasi: x = {root:.3f}")
