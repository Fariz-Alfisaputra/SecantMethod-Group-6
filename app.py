import matplotlib
matplotlib.use('Agg') #Ini penting untuk server, agar matplotlib tidak mencoba membuka GUI

from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

PRESET_FUNCTIONS = {
    "f(x) = x³ - x - 2": "x**3 - x - 2",
    "f(x) = cos(x) - x": "cos(x) - x",
    "f(x) = e⁻ˣ - x": "exp(-x) - x",
    "f(x) = x² - 4": "x**2 - 4"
}

def safe_eval(expr, x_val):
    allowed_names = {
        "x": x_val, "np": np, "sin": np.sin, "cos": np.cos,
        "tan": np.tan, "sqrt": np.sqrt, "exp": np.exp,
        "log": np.log, "log10": np.log10, "abs": np.abs,
        "pi": np.pi, "e": np.e
    }
    code = compile(expr, "<string>", "eval")
    for name in code.co_names:
        if name not in allowed_names:
            raise NameError(f"Fungsi atau variabel '{name}' tidak diizinkan.")
    return eval(code, {"__builtins__": {}}, allowed_names)

def secant_method(func_str, x0, x1, tol, max_iter=100):
    iterations_data = []
    try:
        fx0 = safe_eval(func_str, x0)
        fx1 = safe_eval(func_str, x1)
    except Exception as e:
        return None, f"Error saat evaluasi fungsi awal: {e}", []

    for i in range(1, max_iter + 1):
        if abs(fx1 - fx0) < 1e-15:
            return None, "Pembagi terlalu kecil, metode gagal.", iterations_data
            
        x_next = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        error = abs(x_next - x1)

        iterations_data.append({
            "iter": i, "x0": x0, "x1": x1, "fx0": fx0,
            "fx1": fx1, "x_next": x_next, "error": error
        })
        
        if error < tol:
            return x_next, "Solusi ditemukan.", iterations_data
            
        x0, x1 = x1, x_next
        try:
            fx0, fx1 = fx1, safe_eval(func_str, x_next)
        except Exception as e:
            return None, f"Error saat evaluasi fungsi pada iterasi ke-{i}: {e}", iterations_data

    return None, "Metode tidak konvergen setelah maksimum iterasi.", iterations_data


# =========================================================
def create_plot(func_str, x0, x1, root):
    try:
        plot_points = sorted([x0, x1, root])
        plot_min = plot_points[0] - 2
        plot_max = plot_points[-1] + 2
        
        x_vals = np.linspace(plot_min, plot_max, 400)
        y_vals = np.array([safe_eval(func_str, x) for x in x_vals])
        
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.plot(x_vals, y_vals, label=f'f(x)')
        ax.axhline(0, color='gray', linewidth=0.7)
        ax.axvline(0, color='gray', linewidth=0.7)
        
        if root is not None:
            ax.plot(root, 0, 'ro', markersize=8, label=f'Akar ≈ {root:.6f}')
            
        ax.set_title("Grafik Fungsi dan Akarnya")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        plt.close(fig)
        buf.seek(0)
        
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return image_base64
    except Exception as e:
        print(f"Error saat membuat plot: {e}") #Ini untuk debugging
        return None
# =========================================================


@app.route("/", methods=["GET", "POST"])
def index():
    context = {
        "preset_functions": PRESET_FUNCTIONS,
        "result": None, "message": "", "iterations_data": [],
        "function_str": list(PRESET_FUNCTIONS.values())[0],
        "x0": "1.0", "x1": "2.0", "tol": "0.00001",
        "plot_url": None
    }

    if request.method == "POST":
        preset_choice = request.form.get("function_preset")
        custom_function = request.form.get("function_custom")

        if preset_choice == "custom" and custom_function:
            context["function_str"] = custom_function
        else:
            context["function_str"] = preset_choice

        context["x0"] = request.form.get("x0")
        context["x1"] = request.form.get("x1")
        context["tol"] = request.form.get("tolerance")
        
        try:
            x0 = float(context["x0"])
            x1 = float(context["x1"])
            tol = float(context["tol"])
            
            result, message, iterations_data = secant_method(context["function_str"], x0, x1, tol)
            
            context.update({
                "result": result,
                "message": message,
                "iterations_data": iterations_data
            })
            
            if result is not None:
                context["plot_url"] = create_plot(context["function_str"], x0, x1, result)
    
        except (ValueError, TypeError):
            context["message"] = "Input tidak valid. Pastikan semua angka dimasukkan dengan benar."
        except Exception as e:
            context["message"] = f"Terjadi kesalahan: {e}"

    return render_template("index.html", **context)

if __name__ == "__main__":
    app.run(debug=True)

