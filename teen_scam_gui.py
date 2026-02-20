import tkinter as tk
from scam_detector import analyze_message

def scan_message():
    msg = entry.get()
    risk, score, reasons = analyze_message(msg)

    result_text = f"{risk}\nRisk Score: {score}\n\nReasons:\n"
    for r in reasons:
        result_text += "- " + r + "\n"

    result_label.config(text=result_text)

    # Turn red if scam
    if "HIGH RISK" in risk or "POSSIBLE" in risk:
        result_label.config(fg="red")
    else:
        result_label.config(fg="green")

def delete_message():
    entry.delete(0, tk.END)
    result_label.config(text="Message deleted ❌", fg="blue")

root = tk.Tk()
root.title("TeenShield Security Alert")
root.geometry("500x350")
root.configure(bg="black")

title = tk.Label(root, text="🚨 TeenShield Scam Detector", font=("Arial", 18), fg="red", bg="black")
title.pack(pady=10)

entry = tk.Entry(root, width=60)
entry.pack(pady=10)

scan_button = tk.Button(root, text="Scan Message", command=scan_message, bg="orange")
scan_button.pack(pady=5)

delete_button = tk.Button(root, text="DELETE MESSAGE", command=delete_message, bg="red", fg="white")
delete_button.pack(pady=5)

result_label = tk.Label(root, text="", wraplength=450, justify="left", bg="black", fg="white")
result_label.pack(pady=10)

root.mainloop()
