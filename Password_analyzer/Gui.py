import tkinter as tk
from tkinter import ttk
from analyzer import analyze_password, recommend, generate_strong_password

def check_password():
    pwd = entry.get()
    result = analyze_password(pwd)
    suggestions = recommend(pwd)

    result_text = f"""
Password Strength: {result['strength']}
Length: {result['length']}
Entropy: {result['entropy']} bits
Contains Uppercase: {result['has_upper']}
Contains Lowercase: {result['has_lower']}
Contains Digits: {result['has_digit']}
Contains Symbols: {result['has_symbol']}
"""

    if result['weaknesses']:
        weaknesses = "\n".join(f"- {w}" for w in result['weaknesses'])
        result_text += f"\nDetected Weaknesses:\n{weaknesses}"
    else:
        result_text += "\nNo major weaknesses detected."

    result_label.config(text=result_text.strip())
    suggestion_label.config(text="\n".join(suggestions))

def generate_password():
    new_pwd = generate_strong_password()
    entry.delete(0, tk.END)
    entry.insert(0, new_pwd)
    check_password()

def toggle_password_visibility():
    if show_password_var.get():
        entry.config(show="")
    else:
        entry.config(show="*")

def reset_fields():
    entry.delete(0, tk.END)
    result_label.config(text="")
    suggestion_label.config(text="")
    show_password_var.set(False)
    entry.config(show="*")

# GUI Setup
window = tk.Tk()
window.title("Password Strength Analyzer")
window.geometry("550x520")
window.resizable(False, False)

title = ttk.Label(window, text="🔐 Password Strength Analyzer", font=("Arial", 16, "bold"))
title.pack(pady=10)

entry_label = ttk.Label(window, text="Enter Password:", font=("Arial", 12))
entry_label.pack(pady=5)

entry = ttk.Entry(window, width=40, show="*")
entry.pack()

show_password_var = tk.BooleanVar(value=False)
show_checkbox = ttk.Checkbutton(
    window, text="Show Password", variable=show_password_var, command=toggle_password_visibility
)
show_checkbox.pack(pady=3)

analyze_btn = ttk.Button(window, text="Analyze Password", command=check_password)
analyze_btn.pack(pady=10)

generate_btn = ttk.Button(window, text="Generate Strong Password", command=generate_password)
generate_btn.pack(pady=5)

reset_btn = ttk.Button(window, text="Reset", command=reset_fields)
reset_btn.pack(pady=5)

result_label = ttk.Label(window, text="", justify="left", font=("Courier", 12), foreground="light blue", wraplength=500)
result_label.pack(pady=10)

suggestion_title = ttk.Label(window, text="Suggestions:", font=("Arial", 14, "underline"))
suggestion_title.pack(pady=5)

suggestion_label = ttk.Label(window, text="", justify="left", font=("Arial", 12), foreground="red", wraplength=500)
suggestion_label.pack(pady=5)

window.mainloop()
