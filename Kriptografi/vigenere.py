import tkinter as tk
from tkinter import filedialog, messagebox

# Fungsi untuk Vigenere Cipher
def vigenere_cipher(text, key, encrypt=True):
    key = key.upper()
    text = text.upper()
    result = []
    
    key_length = len(key)
    key_as_int = [ord(i) - ord('A') for i in key]
    text_as_int = [ord(i) - ord('A') for i in text if i.isalpha()]
    
    for i in range(len(text_as_int)):
        if encrypt:
            value = (text_as_int[i] + key_as_int[i % key_length]) % 26
        else:
            value = (text_as_int[i] - key_as_int[i % key_length]) % 26
        result.append(chr(value + ord('A')))
    
    return ''.join(result)

# Fungsi untuk membuka file
def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, 'r') as file:
            content.set(file.read())

# Fungsi untuk validasi kunci
def validate_key(key):
    if len(key) < 12:
        messagebox.showerror("Error", "Kunci harus memiliki minimal 12 karakter!")
        return False
    return True

# Fungsi untuk mengenkripsi atau mendekripsi
def process_cipher(encrypt=True):
    text = content.get("1.0", tk.END).strip()
    key = key_input.get().strip()
    
    if not validate_key(key):
        return
    
    result = vigenere_cipher(text, key, encrypt)
    output.set(result)

# GUI setup
root = tk.Tk()
root.title("Vigenere Cipher")

# Mengatur ukuran jendela dan warna background
root.geometry("600x400")
root.configure(bg="#e6e6e6")

font_label = ("Arial", 12, "bold")
font_entry = ("Arial", 10)
bg_color = "#ffffff"
button_color = "#007acc"
button_fg = "#ffffff"

# Frame utama
frame = tk.Frame(root, padx=10, pady=10, bg="#e6e6e6")
frame.pack()

# Label dan Textbox untuk input
tk.Label(frame, text="Input Text:", font=font_label, bg="#e6e6e6").grid(row=0, column=0, columnspan=2)
content = tk.Text(frame, height=10, width=60, bg=bg_color, font=font_entry)
content.grid(row=1, column=0, columnspan=2, pady=10)

# Tombol untuk upload file
tk.Button(frame, text="Upload File", command=open_file, bg=button_color, fg=button_fg, font=font_entry).grid(row=2, column=0, columnspan=2, pady=5)

# Input untuk kunci
tk.Label(frame, text="Enter Key (min 12 chars):", font=font_label, bg="#e6e6e6").grid(row=3, column=0, pady=5)
key_input = tk.Entry(frame, width=50, font=font_entry)
key_input.grid(row=3, column=1, pady=5)

# Tombol enkripsi dan dekripsi
tk.Button(frame, text="Encrypt", command=lambda: process_cipher(True), bg="#4caf50", fg=button_fg, font=font_entry).grid(row=4, column=0, pady=10, ipadx=10)
tk.Button(frame, text="Decrypt", command=lambda: process_cipher(False), bg="#ff5722", fg=button_fg, font=font_entry).grid(row=4, column=1, pady=10, ipadx=10)

# Output teks
output = tk.StringVar()
tk.Label(frame, text="Output:", font=font_label, bg="#e6e6e6").grid(row=5, column=0, pady=5)
tk.Entry(frame, textvariable=output, width=60, font=font_entry, bg=bg_color).grid(row=6, column=0, columnspan=2, pady=5)

# Menjalankan GUI
root.mainloop()
