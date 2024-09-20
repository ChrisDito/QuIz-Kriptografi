import numpy as np
import tkinter as tk
from tkinter import messagebox

# Substitution dictionary for mapping letters to numbers
substitution = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9,
               'K': 10, 'L': 11, 'M': 12, 'N': 13, 'O': 14, 'P': 15, 'Q': 16, 'R': 17, 'S': 18,
               'T': 19, 'U': 20, 'V': 21, 'W': 22, 'X': 23, 'Y': 24, 'Z': 25}

# Inverse substitution dictionary for mapping numbers to letters
inverse_substitution = {value: key for key, value in substitution.items()}

# Function for encryption
def encrypt(plain_text, key_matrix):
    plain_text = plain_text.upper()
    plain_text = plain_text.replace(" ", "")
    
    # Pad the plain text if its length is not a multiple of the key matrix size
    if len(plain_text) % len(key_matrix) != 0:
        padding_length = len(key_matrix) - (len(plain_text) % len(key_matrix))
        plain_text += 'X' * padding_length

    cipher_text = ''

    # Encrypt the plain text block by block
    for i in range(0, len(plain_text), len(key_matrix)):
        block = plain_text[i:i+len(key_matrix)]
        block_vector = np.array([substitution[ch] for ch in block])
        encrypted_vector = np.dot(key_matrix, block_vector) % 26
        encrypted_block = ''.join([inverse_substitution[num] for num in encrypted_vector])
        cipher_text += encrypted_block

    return cipher_text

# Function for decryption
def decrypt(cipher_text, key_matrix):
    cipher_text = cipher_text.upper().replace(" ", "")
    
    # Calculate the determinant of the key matrix
    det = int(np.round(np.linalg.det(key_matrix)))
    inv_det = pow(det, -1, 26)  # Find modular inverse of determinant

    # Calculate the inverse of the key matrix
    adj_matrix = np.round(np.linalg.inv(key_matrix) * det).astype(int) % 26
    inv_key_matrix = (inv_det * adj_matrix) % 26

    plain_text = ''

    # Decrypt the cipher text block by block
    for i in range(0, len(cipher_text), len(key_matrix)):
        block = cipher_text[i:i+len(key_matrix)]
        block_vector = np.array([substitution[ch] for ch in block])
        decrypted_vector = np.dot(inv_key_matrix, block_vector) % 26
        decrypted_block = ''.join([inverse_substitution[num] for num in decrypted_vector])
        plain_text += decrypted_block

    return plain_text

# Create the key matrix from user input of numbers
def create_key_matrix(key):
    try:
        # Split the key input by spaces and convert each part into an integer
        key_numbers = list(map(int, key.split()))
        
        # Ensure that we have exactly 9 numbers for a 3x3 matrix
        if len(key_numbers) != 9:
            messagebox.showerror("Error", "Key must have exactly 9 numbers!")
            return None
        
        # Reshape the list of numbers into a 3x3 matrix
        key_matrix = np.array(key_numbers).reshape(3, 3)
        return key_matrix
    except ValueError:
        messagebox.showerror("Error", "Key must contain only numbers!")
        return None

# Encrypt button callback
def encrypt_callback():
    plain_text = input_text.get("1.0", "end-1c")  # Get the plain text from Text widget
    key = key_input.get()  # Get the key from Entry widget

    key_matrix = create_key_matrix(key)
    if key_matrix is None:
        return  # If key is invalid, return early

    # Encrypt the plain text
    cipher_text = encrypt(plain_text, key_matrix)
    output_text.set(cipher_text)  # Display the result in the output field

# Decrypt button callback
def decrypt_callback():
    cipher_text = input_text.get("1.0", "end-1c")  # Get the cipher text from Text widget
    key = key_input.get()  # Get the key from Entry widget

    key_matrix = create_key_matrix(key)
    if key_matrix is None:
        return  # If key is invalid, return early

    # Decrypt the cipher text
    plain_text = decrypt(cipher_text, key_matrix)
    output_text.set(plain_text)  # Display the result in the output field

# GUI setup
root = tk.Tk()
root.title("Hill Cipher Encryption & Decryption")

# Configure window size and background color
root.geometry("500x400")
root.configure(bg="#e6e6e6")

# Font and color settings
font_label = ("Arial", 12, "bold")
font_entry = ("Arial", 10)
bg_color = "#ffffff"
button_color = "#007acc"
button_fg = "#ffffff"

# Frame for main layout
frame = tk.Frame(root, padx=10, pady=10, bg="#e6e6e6")
frame.pack()

# Input text label and text box
tk.Label(frame, text="Input Text:", font=font_label, bg="#e6e6e6").grid(row=0, column=0, pady=5)
input_text = tk.Text(frame, height=5, width=40, bg=bg_color, font=font_entry)
input_text.grid(row=1, column=0, columnspan=2, pady=5)

# Key input label and entry
tk.Label(frame, text="Key (3 x 3 matrix):", font=font_label, bg="#e6e6e6").grid(row=2, column=0, pady=5)
key_input = tk.Entry(frame, width=40, font=font_entry)
key_input.grid(row=2, column=1, pady=5)

# Encrypt and Decrypt buttons
tk.Button(frame, text="Encrypt", command=encrypt_callback, bg=button_color, fg=button_fg, font=font_entry).grid(row=3, column=0, pady=10, ipadx=10)
tk.Button(frame, text="Decrypt", command=decrypt_callback, bg="#ff5722", fg=button_fg, font=font_entry).grid(row=3, column=1, pady=10, ipadx=10)

# Output text label and entry for displaying result
tk.Label(frame, text="Output Text:", font=font_label, bg="#e6e6e6").grid(row=4, column=0, pady=5)
output_text = tk.StringVar()
tk.Entry(frame, textvariable=output_text, width=40, font=font_entry, bg=bg_color).grid(row=5, column=0, columnspan=2, pady=5)

# Run the GUI
root.mainloop()
