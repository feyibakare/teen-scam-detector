import tkinter as tk
from scam_detector import analyze_message

def check_message():
    msg = text_input.get("1.0", tk.END)
    risk, score, reasons = analyze_message(msg)

    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, f"{risk}\n")
    result_box.insert(tk.END, f"Risk Score: {score}\n\n")
    for r in reasons:
        result_box.insert(tk.END, "- " + r + "\n")

# Window
root = tk.Tk()
root.title("Teen Scam Detector")
root.geometry("500x400")

# Title
title = tk.Label(root, text="Teen Scam Detector", font=("Arial", 16))
title.pack()

# Input box
text_input = tk.Text(root, height=5)
text_input.pack()

# Button
check_button = tk.Button(root, text="Scan Message", command=check_message)
check_button.pack()

# Output box
result_box = tk.Text(root, height=10)
result_box.pack()

root.mainloop()
