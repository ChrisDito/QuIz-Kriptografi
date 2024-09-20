import tkinter as tk
from tkinter import filedialog, messagebox

# Fungsi untuk memformat kunci Playfair dan membuat matriks 5x5
def generate_key_matrix(key):
    key = key.upper().replace('J', 'I')
    key = ''.join(sorted(set(key), key=lambda x: key.index(x)))
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
    key_matrix = [char for char in key if char in alphabet]
    for char in alphabet:
        if char not in key_matrix:
            key_matrix.append(char)
    return [key_matrix[i:i+5] for i in range(0, 25, 5)]

# Fungsi untuk memformat teks untuk Playfair Cipher (hilangkan non-alphabet dan tambahkan padding 'X' jika diperlukan)
def format_text(text):
    text = text.upper().replace('J', 'I')
    text = ''.join([char for char in text if char.isalpha()])
    formatted_text = ""
    i = 0
    while i < len(text):
        formatted_text += text[i]
        if i + 1 < len(text) and text[i] == text[i + 1]:
            formatted_text += 'X'
        elif i + 1 < len(text):
            formatted_text += text[i + 1]
        i += 2
    if len(formatted_text) % 2 != 0:
        formatted_text += 'X'
    return formatted_text

# Fungsi untuk mengenkripsi menggunakan Playfair Cipher
def playfair_encrypt(text, key_matrix):
    text = format_text(text)
    encrypted_text = ""
    
    for i in range(0, len(text), 2):
        char1, char2 = text[i], text[i+1]
        row1, col1 = find_position(char1, key_matrix)
        row2, col2 = find_position(char2, key_matrix)
        
        if row1 == row2:
            encrypted_text += key_matrix[row1][(col1 + 1) % 5]
            encrypted_text += key_matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted_text += key_matrix[(row1 + 1) % 5][col1]
            encrypted_text += key_matrix[(row2 + 1) % 5][col2]
        else:
            encrypted_text += key_matrix[row1][col2]
            encrypted_text += key_matrix[row2][col1]
    
    return encrypted_text

# Fungsi untuk mendekripsi menggunakan Playfair Cipher
def playfair_decrypt(text, key_matrix):
    decrypted_text = ""
    
    for i in range(0, len(text), 2):
        char1, char2 = text[i], text[i+1]
        row1, col1 = find_position(char1, key_matrix)
        row2, col2 = find_position(char2, key_matrix)
        
        if row1 == row2:
            decrypted_text += key_matrix[row1][(col1 - 1) % 5]
            decrypted_text += key_matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            decrypted_text += key_matrix[(row1 - 1) % 5][col1]
            decrypted_text += key_matrix[(row2 - 1) % 5][col2]
        else:
            decrypted_text += key_matrix[row1][col2]
            decrypted_text += key_matrix[row2][col1]
    
    return clean_decrypted_text(decrypted_text)

# Fungsi untuk membersihkan teks hasil dekripsi dari padding 'X' yang tidak relevan
def clean_decrypted_text(text):
    cleaned_text = ""
    i = 0
    while i < len(text):
        cleaned_text += text[i]
        if i + 1 < len(text) and text[i] == text[i + 1] and text[i + 1] == 'X':
            i += 2  # Lewati huruf 'X' yang tidak relevan
        else:
            i += 1
    return cleaned_text

# Fungsi untuk menemukan posisi karakter di dalam matriks kunci
def find_position(char, key_matrix):
    for row in range(5):
        if char in key_matrix[row]:
            return row, key_matrix[row].index(char)

# Fungsi untuk membuka file
def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, 'r') as file:
            content.set(file.read())

# Fungsi validasi kunci
def validate_key(key):
    if len(key) < 12:
        messagebox.showerror("Error", "Kunci harus memiliki minimal 12 karakter!")
        return False
    return True

# Fungsi untuk mengenkripsi atau mendekripsi
def process_cipher(encrypt=True):
    text = content.get("1.0", tk.END).strip()
    key_input_text = key_input.get().strip()
    
    if not validate_key(key_input_text):
        return
    
    try:
        # Membuat matriks kunci
        key_matrix = generate_key_matrix(key_input_text)
        
        if encrypt:
            result = playfair_encrypt(text, key_matrix)
        else:
            result = playfair_decrypt(text, key_matrix)
        
        output.set(result)
    except ValueError:
        messagebox.showerror("Error", "Format kunci tidak valid!")
        
# GUI setup
root = tk.Tk()
root.title("Playfair Cipher")

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
