import tkinter as tk
import os
import time
from threading import Thread

SECRET_KEY = "unlock123"

def fake_ransomware():
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    root.title("CrypterX - Files Encrypted")

    tk.Label(root, text="YOUR FILES ARE ENCRYPTED", fg="red", bg="black",
             font=("Arial", 40, "bold")).pack(pady=40)
    tk.Label(root, text="Send 0.2 BTC to 1FAKEr4ns0mWa11e7x to recover your data.",
             fg="white", bg="black", font=("Arial", 18)).pack(pady=20)
    countdown_label = tk.Label(root, text="", fg="cyan", bg="black", font=("Arial", 16))
    countdown_label.pack(pady=10)

    entry = tk.Entry(root, font=("Arial", 16), show="*")
    entry.pack(pady=20)

    def check_code(event=None):
        if entry.get() == SECRET_KEY:
            root.destroy()

    entry.bind("<Return>", check_code)

    def countdown(t):
        while t:
            mins, secs = divmod(t, 60)
            countdown_label.config(text=f"Time remaining: {mins:02d}:{secs:02d}")
            time.sleep(1)
            t -= 1
        countdown_label.config(text="TIME'S UP!")

    Thread(target=countdown, args=(600,), daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    fake_ransomware()
