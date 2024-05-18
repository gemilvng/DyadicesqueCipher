import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import os

# Create the main window
root = tk.Tk()
root.title("Bernoulli Shift Image Encryption")

# Frames for organization
topFrame = tk.Frame(root)
topFrame.pack()

middleFrame = tk.Frame(root)
middleFrame.pack(side=tk.BOTTOM)

bottomFrame = tk.Frame(root)
bottomFrame.pack(side=tk.BOTTOM)

encryptionFrame = tk.Frame(root)
encryptionFrame.pack(side=tk.BOTTOM)

# Functions for image encryption and decryption
def bernoulli_shift(x, n):
    trajectory = np.empty(n)
    for i in range(n):
        x = (2 * x) % 1
        trajectory[i] = x
    return trajectory

def generate_indices(seed, size):
    trajectory = bernoulli_shift(seed, size)
    indices = np.argsort(trajectory)
    return indices

def shuffle_image(image, indices):
    img_array = np.array(image)
    flat_img_array = img_array.flatten()
    shuffled_flat_img = flat_img_array[indices]
    shuffled_img = shuffled_flat_img.reshape(img_array.shape)
    return Image.fromarray(shuffled_img)

def unshuffle_image(image, indices):
    img_array = np.array(image)
    flat_img_array = img_array.flatten()
    unshuffled_flat_img = np.empty_like(flat_img_array)
    unshuffled_flat_img[indices] = flat_img_array
    unshuffled_img = unshuffled_flat_img.reshape(img_array.shape)
    return Image.fromarray(unshuffled_img)

def choose_File():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        entry1.delete(0, tk.END)
        entry1.insert(0, file_path)
        load_and_display_image(file_path, original_image_label)

def load_and_display_image(image_path, label):
    image = Image.open(image_path).convert('L')
    display_image(label, image)
    label.image = image

def performEncryption():
    file_path = entry1.get()
    if not file_path:
        error_label.config(text="No image selected.")
        return
    
    try:
        seed = float(entry_seed.get())
        iterations = int(entry_iterations.get())
    except ValueError:
        error_label.config(text="Invalid input values.")
        return

    image = Image.open(file_path).convert('L')
    width, height = image.size
    size = width * height
    indices = generate_indices(seed, size)

    for _ in range(iterations):
        image = shuffle_image(image, indices)

    save_image(image, "encrypted_image.bmp")
    entry2.delete(0, tk.END)
    entry2.insert(0, os.path.abspath("encrypted_image.bmp"))
    display_image(encrypted_image_label, image)

def performDecryption():
    file_path = entry2.get()
    if not file_path:
        error_label.config(text="No encrypted image selected.")
        return
    
    try:
        seed = float(entry_seed.get())
        iterations = int(entry_iterations.get())
    except ValueError:
        error_label.config(text="Invalid input values.")
        return

    image = Image.open(file_path).convert('L')
    width, height = image.size
    size = width * height
    indices = generate_indices(seed, size)

    for _ in range(iterations):
        image = unshuffle_image(image, indices)

    save_image(image, "decrypted_image.bmp")
    entry4.delete(0, tk.END)
    entry4.insert(0, os.path.abspath("decrypted_image.bmp"))
    display_image(decrypted_image_label, image)

def save_image(image, output_path):
    image.save(output_path)

def display_image(label, image):
    img_display = ImageTk.PhotoImage(image)
    label.config(image=img_display)
    label.image = img_display

def openFileForViewing(entry):
    file_path = entry.get()
    if os.path.exists(file_path):
        os.startfile(file_path)

# Widgets
label_seed = tk.Label(topFrame, text="Seed (float):")
entry_seed = tk.Entry(topFrame)

label_iterations = tk.Label(topFrame, text="Iterations:")
entry_iterations = tk.Entry(topFrame)

label_image = tk.Label(topFrame, text="Image to be Encrypted: ")
entry1 = tk.Entry(topFrame, width=50)
button1 = tk.Button(topFrame, text="Select Image", command=choose_File)

button_encrypt = tk.Button(middleFrame, text="Encrypt Image", command=performEncryption)
entry2 = tk.Entry(middleFrame, width=50)
button_open_encrypted = tk.Button(middleFrame, text="Open Encrypted Image", command=lambda: openFileForViewing(entry2))

button_decrypt = tk.Button(encryptionFrame, text="Decrypt Image", command=performDecryption)
entry4 = tk.Entry(encryptionFrame, width=50)
button_open_decrypted = tk.Button(encryptionFrame, text="Open Decrypted Image", command=lambda: openFileForViewing(entry4))

error_label = tk.Label(root, text="", fg="red")

# Image display labels
original_image_label = tk.Label(root)
encrypted_image_label = tk.Label(root)
decrypted_image_label = tk.Label(root)

# Layout
label_seed.pack(side=tk.TOP)
entry_seed.pack(side=tk.TOP)

label_iterations.pack(side=tk.TOP)
entry_iterations.pack(side=tk.TOP)

label_image.pack(side=tk.TOP)
entry1.pack(side=tk.TOP)
button1.pack(side=tk.TOP)

button_encrypt.pack(side=tk.LEFT)
entry2.pack(side=tk.LEFT)
button_open_encrypted.pack(side=tk.LEFT)

button_decrypt.pack(side=tk.LEFT)
entry4.pack(side=tk.LEFT)
button_open_decrypted.pack(side=tk.LEFT)

error_label.pack(side=tk.TOP)

original_image_label.pack(side=tk.LEFT, padx=5, pady=5)
encrypted_image_label.pack(side=tk.LEFT, padx=5, pady=5)
decrypted_image_label.pack(side=tk.LEFT, padx=5, pady=5)

# Start the main loop
root.mainloop()
