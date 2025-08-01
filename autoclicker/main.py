import pyautogui
import threading
import time
import tkinter as tk
from tkinter import messagebox
import keyboard

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")

        # Set pink background for the main window
        self.root.configure(bg="#ffc0cb")  # light pink

        self.clicking = False
        self.thread = None

        # Label with pink background and custom font color
        tk.Label(root, text="Click Interval (seconds):", bg="#ffc0cb", fg="#800080", font=("Arial", 12, "bold")).pack(pady=5)

        self.interval_entry = tk.Entry(root, bg="#ffe4e1", fg="#800080", font=("Arial", 12))
        self.interval_entry.insert(0, "1.0")
        self.interval_entry.pack()

        self.status_label = tk.Label(root, text="Status: Stopped", fg="red", bg="#ffc0cb", font=("Arial", 12, "bold"))
        self.status_label.pack(pady=5)

        self.start_button = tk.Button(root, text="Start Clicking", command=self.start_clicking,
                                      bg="#ff69b4", fg="white", font=("Arial", 12, "bold"))
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Clicking", command=self.stop_clicking, state=tk.DISABLED,
                                     bg="#ff1493", fg="white", font=("Arial", 12, "bold"))
        self.stop_button.pack(pady=5)

        # Listen for F6 hotkey to toggle clicking
        keyboard.add_hotkey('F6', self.toggle_clicking)

    def click_loop(self, interval):
        while self.clicking:
            pyautogui.click()
            time.sleep(interval)

    def start_clicking(self):
        try:
            interval = float(self.interval_entry.get())
            if interval <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a positive number for the interval.")
            return

        if not self.clicking:
            self.clicking = True
            self.status_label.config(text="Status: Clicking...", fg="green")
            self.thread = threading.Thread(target=self.click_loop, args=(interval,), daemon=True)
            self.thread.start()
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_clicking(self):
        self.clicking = False
        self.status_label.config(text="Status: Stopped", fg="red")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def toggle_clicking(self):
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
