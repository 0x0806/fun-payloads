import tkinter as tk
import os
import time
import random
from threading import Thread

# --- Settings ---
SECRET_KEY = "unlock123"
BRANDING = "CrypterX by 0x0806"
SIMULATED_FILES = [f"important_file_{i}.docx" for i in range(1, 25)]

# --- Simulate Fake Encryption ---
def simulate_file_encryption(output_widget):
    for file in SIMULATED_FILES:
        time.sleep(0.15)
        output_widget.insert(tk.END, f"[+] Encrypting: {file}\n")
        output_widget.see(tk.END)

# --- Main Ransomware Window ---
def fake_ransomware():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    root.title("CrypterX - Files Encrypted")

    tk.Label(root, text="YOUR FILES HAVE BEEN ENCRYPTED", fg="red", bg="black",
             font=("Courier", 40, "bold")).pack(pady=30)
    tk.Label(root, text="Send 0.2 BTC to recover your data", fg="white", bg="black",
             font=("Courier", 18)).pack()
    tk.Label(root, text="Wallet: 1FAKEr4ns0mWa11e7x", fg="cyan", bg="black",
             font=("Courier", 18)).pack(pady=10)

    # Countdown label
    countdown_label = tk.Label(root, text="", fg="orange", bg="black", font=("Courier", 16))
    countdown_label.pack(pady=10)

    # Simulated output
    output_box = tk.Text(root, height=10, width=80, bg="black", fg="lime", font=("Courier", 12))
    output_box.pack(pady=20)

    # Unlock entry
    entry = tk.Entry(root, font=("Courier", 18), show="*", justify="center", width=20)
    entry.pack()

    def check_code(event=None):
        if entry.get() == SECRET_KEY:
            root.destroy()

    entry.bind("<Return>", check_code)

    # Countdown logic
    def countdown(t):
        while t:
            mins, secs = divmod(t, 60)
            countdown_label.config(text=f"Time remaining: {mins:02d}:{secs:02d}")
            time.sleep(1)
            t -= 1
        countdown_label.config(text="TIME'S UP — FILES LOST")

    # Start encryption + timer
    Thread(target=simulate_file_encryption, args=(output_box,), daemon=True).start()
    Thread(target=countdown, args=(600,), daemon=True).start()

    # Branding
    tk.Label(root, text=BRANDING, fg="gray", bg="black", font=("Courier", 10)).pack(side="bottom", pady=5)

    root.mainloop()

# --- Launch ---
if __name__ == "__main__":
    fake_ransomware()
