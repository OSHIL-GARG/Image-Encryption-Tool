import os
from tkinter import Tk, Button, Label, Entry, filedialog, messagebox
from PIL import Image
import random

# Get seeded random generator
def get_seeded_random(seed):
    """Returns a seeded random generator."""
    return random.Random(seed)

# Encrypt image by shuffling pixels
def encrypt_image(input_image_path, output_image_path, seed):
    try:
        image = Image.open(input_image_path)
        width, height = image.size
        pixels = list(image.getdata())

        random_gen = get_seeded_random(seed)
        indices = list(range(len(pixels)))
        random_gen.shuffle(indices)

        encrypted_pixels = [pixels[i] for i in indices]
        encrypted_image = Image.new(image.mode, (width, height))
        encrypted_image.putdata(encrypted_pixels)
        encrypted_image.save(output_image_path)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Encryption Failed:\n{str(e)}")
        return False

# Decrypt image by reversing pixel shuffle
def decrypt_image(input_image_path, output_image_path, seed):
    try:
        image = Image.open(input_image_path)
        width, height = image.size
        encrypted_pixels = list(image.getdata())

        random_gen = get_seeded_random(seed)
        indices = list(range(len(encrypted_pixels)))
        random_gen.shuffle(indices)

        decrypted_pixels = [None] * len(encrypted_pixels)
        for original_index, shuffled_index in enumerate(indices):
            decrypted_pixels[shuffled_index] = encrypted_pixels[original_index]

        decrypted_image = Image.new(image.mode, (width, height))
        decrypted_image.putdata(decrypted_pixels)
        decrypted_image.save(output_image_path)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Decryption Failed:\n{str(e)}")
        return False

# GUI: Select input image
def select_input_image():
    input_path = filedialog.askopenfilename(title="Select Image")
    input_image_label.config(text=input_path)

# GUI: Select output image location
def select_output_image():
    output_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg"), ("All files", "*.*")],
        title="Save Encrypted/Decrypted Image"
    )
    output_image_label.config(text=output_path)

# GUI: Encrypt image button action
def encrypt():
    input_image_path = input_image_label.cget("text")
    output_image_path = output_image_label.cget("text")
    seed = seed_entry.get()

    if not input_image_path or not output_image_path or not seed:
        messagebox.showerror("Error", "Please provide all inputs and a seed key.")
        return

    if encrypt_image(input_image_path, output_image_path, seed):
        messagebox.showinfo("Success", "Image encrypted successfully!")

# GUI: Decrypt image button action
def decrypt():
    input_image_path = input_image_label.cget("text")
    output_image_path = output_image_label.cget("text")
    seed = seed_entry.get()

    if not input_image_path or not output_image_path or not seed:
        messagebox.showerror("Error", "Please provide all inputs and a seed key.")
        return

    if decrypt_image(input_image_path, output_image_path, seed):
        messagebox.showinfo("Success", "Image decrypted successfully!")

# === GUI Setup ===
root = Tk()
root.title("Image Encryption Tool")
root.geometry("400x350")
root.resizable(False, False)

# Widgets
Label(root, text="Select Image to Encrypt/Decrypt:", font=("Arial", 10)).pack(pady=5)
input_image_label = Label(root, text="No image selected", fg="gray")
input_image_label.pack(pady=5)
Button(root, text="Browse", command=select_input_image).pack(pady=5)

Label(root, text="Output Image Path:", font=("Arial", 10)).pack(pady=5)
output_image_label = Label(root, text="No output path selected", fg="gray")
output_image_label.pack(pady=5)
Button(root, text="Save As", command=select_output_image).pack(pady=5)

Label(root, text="Enter Seed Key:", font=("Arial", 10)).pack(pady=5)
seed_entry = Entry(root)
seed_entry.pack(pady=5)

Button(root, text="Encrypt Image", command=encrypt, bg="#4CAF50", fg="white").pack(pady=10)
Button(root, text="Decrypt Image", command=decrypt, bg="#2196F3", fg="white").pack(pady=5)

# Start GUI loop
root.mainloop()
