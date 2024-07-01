import tkinter as tk
import random
import string
import math

class PasswordGenerator:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure Password Generator")

        self.length_label = tk.Label(master, text="Password Length:")
        self.length_label.pack()
        
        self.length_entry = tk.Entry(master, width=10)
        self.length_entry.pack()

        self.options_label = tk.Label(master, text="Include Characters:")
        self.options_label.pack()

        self.include_upper = tk.BooleanVar()
        self.include_lower = tk.BooleanVar()
        self.include_digits = tk.BooleanVar()
        self.include_special = tk.BooleanVar()

        self.upper_check = tk.Checkbutton(master, text="Uppercase (A-Z)", variable=self.include_upper)
        self.upper_check.pack()
        self.lower_check = tk.Checkbutton(master, text="Lowercase (a-z)", variable=self.include_lower)
        self.lower_check.pack()
        self.digits_check = tk.Checkbutton(master, text="Digits (0-9)", variable=self.include_digits)
        self.digits_check.pack()
        self.special_check = tk.Checkbutton(master, text="Special (!@#...)", variable=self.include_special)
        self.special_check.pack()

        self.generate_button = tk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.pack()

        self.password_label = tk.Label(master, text="Generated Password:")
        self.password_label.pack()

        self.password_display = tk.Entry(master, width=50)
        self.password_display.pack()

        self.strength_label = tk.Label(master, text="", fg="blue")
        self.strength_label.pack()

    def generate_password(self):
        length = int(self.length_entry.get())
        char_set = ""
        
        if self.include_upper.get():
            char_set += string.ascii_uppercase
        if self.include_lower.get():
            char_set += string.ascii_lowercase
        if self.include_digits.get():
            char_set += string.digits
        if self.include_special.get():
            char_set += string.punctuation

        if not char_set:
            self.password_display.delete(0, tk.END)
            self.password_display.insert(0, "Select at least one character type!")
            return

        password = ''.join(random.choice(char_set) for _ in range(length))
        self.password_display.delete(0, tk.END)
        self.password_display.insert(0, password)

        strength = self.evaluate_password(password)
        self.strength_label.config(text=strength)

    def evaluate_password(self, password):
        length = len(password)
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in string.punctuation for c in password)
        entropy = self.calculate_entropy(password)

        if length < 6:
            return f"Weak: Too short (entropy: {entropy:.2f} bits)"
        elif length >= 6 and length < 8 and (has_upper or has_lower) and has_digit:
            return f"Weak: Length >= 6 but < 8, and lacks complexity (entropy: {entropy:.2f} bits)"
        elif length >= 8 and (has_upper and has_lower and has_digit and has_special):
            return f"Strong (entropy: {entropy:.2f} bits)"
        else:
            return f"Medium (entropy: {entropy:.2f} bits)"

    def calculate_entropy(self, password):
        charset_size = 0
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in string.punctuation for c in password):
            charset_size += len(string.punctuation)
        
        if charset_size == 0:
            return 0

        entropy = len(password) * math.log2(charset_size)
        return entropy

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop()
