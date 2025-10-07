from flask import Flask, render_template, request
import numpy as np

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
    """
    Modifikasi: Sekarang mengembalikan (hasil, pesan, data_iterasi)
    """
    iterations_data = []  # List untuk menyimpan data setiap iterasi
    
    try:
        fx0 = safe_eval(func_str, x0)
        fx1 = safe_eval(func_str, x1)
    except Exception as e:
        return None, f"Error saat evaluasi fungsi awal: {e}", []

    # Iterasi dimulai dari 1
    for i in range(1, max_iter + 1):
        if abs(fx1 - fx0) < 1e-15:
            return None, "Pembagi terlalu kecil, metode gagal.", iterations_data
            
        x_next = x1 - fx1 * (x1 - x0) / (fx1 - fx0)
        error = abs(x_next - x1)

        # Simpan data iterasi saat ini
        iterations_data.append({
            "iter": i,
            "x0": x0,
            "x1": x1,
            "fx0": fx0,
            "fx1": fx1,
            "x_next": x_next,
            "error": error
        })
        
        if error < tol:
            return x_next, "Solusi ditemukan.", iterations_data
            
        x0, x1 = x1, x_next
        try:
            fx0, fx1 = fx1, safe_eval(func_str, x_next)
        except Exception as e:
            return None, f"Error saat evaluasi fungsi pada iterasi ke-{i}: {e}", iterations_data

    return None, "Metode tidak konvergen setelah maksimum iterasi.", iterations_data

@app.route("/", methods=["GET", "POST"])
def index():
    context = {
        "preset_functions": PRESET_FUNCTIONS,
        "result": None, "message": "", "iterations_data": [],
        "function_str": list(PRESET_FUNCTIONS.values())[0],
        "x0": "1.0", "x1": "2.0", "tol": "0.00001"
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
            
        except (ValueError, TypeError):
            context["message"] = "Input tidak valid. Pastikan semua angka dimasukkan dengan benar."
        except Exception as e:
            context["message"] = f"Terjadi kesalahan: {e}"

    return render_template("index.html", **context)

if __name__ == "__main__":
    app.run(debug=True)
