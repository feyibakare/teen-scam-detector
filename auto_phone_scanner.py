import tkinter as tk
import time
from scam_detector import analyze_message, explain_scam

fake_inbox = [
    "Hey Fridaous, are you coming to school?",
    "URGENT! You won a free iPhone! Click here now!",
    "Your bank account is locked. Verify your password.",
    "Wanna play Roblox later?"
]

def show_popup(message, risk, reasons):
    popup = tk.Tk()
    popup.title("TeenShield Security Alert")
    popup.attributes("-fullscreen", True)  # FULL SCREEN
    popup.configure(bg="black")

    # Big warning title
    title = tk.Label(popup, text="⚠️ DEVICE THREAT DETECTED ⚠️",
                     font=("Arial", 28, "bold"), fg="red", bg="black")
    title.pack(pady=20)

    # Message box
    msg_label = tk.Label(popup, text=f"Suspicious Message Detected:\n\n{message}",
                         font=("Arial", 14), fg="white", bg="black", wraplength=800)
    msg_label.pack(pady=10)

    # Reasons
    reason_text = "Why this is dangerous:\n"
    for r in reasons:
        reason_text += "- " + r + "\n"

    reason_label = tk.Label(popup, text=reason_text, fg="yellow", bg="black",
                            font=("Arial", 12), justify="left")
    reason_label.pack(pady=10)

    explain = explain_scam(reasons)

    explain_label = tk.Label(popup, text=explain, fg="cyan", bg="black", 
                             font=("Arial", 12), justify="left")
    explain_label.pack(pady=10)

    # Buttons
    delete_button = tk.Button(popup, text="🚫 DELETE MESSAGE",
                              font=("Arial", 16), bg="red", fg="white",
                              command=popup.destroy)
    delete_button.pack(pady=10)

    ignore_button = tk.Button(popup, text="Ignore Warning",
                              font=("Arial", 12), bg="gray", fg="white",
                              command=popup.destroy)
    ignore_button.pack()

    popup.mainloop()

# Simulate phone messages
for msg in fake_inbox:
    time.sleep(3)  # wait like real SMS
    risk, score, reasons = analyze_message(msg)

    print("\n📩 New Message:", msg)
    print("Scan Result:", risk)

    if "HIGH RISK" in risk or "POSSIBLE" in risk:
        show_popup(msg, risk, reasons)
