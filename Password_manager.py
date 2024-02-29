import tkinter as tk
from tkinter import simpledialog, messagebox, font
from cryptography.fernet import Fernet
import os
from PIL import Image, ImageTk

# Master password (for demo purposes, use a secure method in real applications)
MASTER_PASSWORD = "Your password here" # Update your password 


def resize_bg_image(event):
    # Open the image file (this should be the original size image)
    img = Image.open("/Users/sergeyakhmerov/Downloads/background.png")
    # Resize the image to match the canvas size
    resized_img = img.resize((event.width, event.height), Image.ANTIALIAS)

    # Update the background image
    global bg_image
    bg_image = ImageTk.PhotoImage(resized_img)
    canvas.itemconfig(bg_img_id, image=bg_image)


def verify_master_password():
    entered_password = simpledialog.askstring("Master Password", "Enter the master password:", show='*')
    if entered_password == MASTER_PASSWORD:
        messagebox.showinfo("Access", "Access is granted")
        return True
    else:
        messagebox.showerror("Access Denied", "Incorrect master password. Access denied.")
        return False


# Function to prompt for master password
def prompt_master_password():
    if not verify_master_password():
        root.destroy()


# Function definitions for your password manager

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    if not os.path.exists("key.key"):
        write_key()
    with open("key.key", "rb") as key_file:
        key = key_file.read()
    return key


key = load_key()
fer = Fernet(key)


def add_entry(account, password):
    with open('passwords.txt', 'a') as f:
        f.write(account + "|" + fer.encrypt(password.encode()).decode() + "\n")


def view_entries():
    entries_list = []
    try:
        with open('passwords.txt', 'r') as f:
            for line in f.readlines():
                if "|" in line:  # Check if the line contains the separator
                    entries_list.append(line.rstrip())
                else:
                    print(f"Skipping malformed line: {line}")
        return entries_list
    except FileNotFoundError:
        print("No passwords stored yet.")
        return []


# Tkinter functions

def add_password():
    account = simpledialog.askstring("Account", "Enter the account name")
    password = simpledialog.askstring("Password", "Enter the password", show='*')
    add_entry(account, password)
    tk.messagebox.showinfo("Info", "Password added successfully!")


def view_passwords():
    entries = view_entries()
    text.delete('1.0', tk.END)  # Clear the text area
    for entry in entries:
        user, passw_encrypted = entry.split("|")
        try:
            passw = fer.decrypt(passw_encrypted.encode()).decode()
            text.insert(tk.END, "User: " + user + " | Password: " + passw + "\n")
        except Exception as e:
            text.insert(tk.END, f"Error decrypting password for {user}: {str(e)}\n")


# Main Window
root = tk.Tk()
root.title("Password Manager")
root.geometry("1000x800")
root.configure(bg='black')

# Create a Canvas for the background image
canvas = tk.Canvas(root)
canvas.pack(fill="both", expand=True)

# Load the background image
bg_image = ImageTk.PhotoImage(file="/Users/sergeyakhmerov/Downloads/background.png")  # Replace with your image path
canvas.create_image(0, 0, image=bg_image, anchor="nw", tags="bg_img")
canvas.tag_lower("bg_img")  # Ensure the image is behind all other widgets

# Hacker-style font
hacker_font = font.Font(family="Courier", size=12)

# Add password button
add_button = tk.Button(root, text="Add New Password", command=add_password, font=hacker_font, fg='green', bg='black')

# View passwords button
view_button = tk.Button(root, text="View Passwords", command=view_passwords, font=hacker_font, fg='green', bg='black')

# Text area for viewing passwords
text = tk.Text(root, height=20, width=100, font=hacker_font, fg='green', bg='black')

# Position widgets on the canvas instead of packing them
canvas.create_window((root.winfo_screenwidth() / 2, 50), window=add_button, anchor="n")
canvas.create_window((root.winfo_screenwidth() / 2, 100), window=view_button, anchor="n")
canvas.create_window((root.winfo_screenwidth() / 2, 150), window=text, anchor="n")

root.bind("<Configure>", resize_bg_image)
# Prompt for master password on startup
root.after(100, prompt_master_password)

# Start the GUI event loop
root.mainloop()
