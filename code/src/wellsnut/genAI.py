import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkhtmlview import HTMLLabel
import pandas as pd
from ydata_profiling import ProfileReport
import openai
import os
import genRegex

# Global variables for file paths
data_file_path = None
rules_file_path = None


def upload_csv(tree):
    """Upload and display CSV file content, store file path."""
    global data_file_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        # Save the file in the specified directory
        destination_path = r"C:\Users\Nareshkumar\OneDrive\Desktop\AI"
        os.makedirs(destination_path, exist_ok=True)  # Create directory if it doesn't exist
        new_file_path = os.path.join(destination_path, os.path.basename(file_path))
        try:
            # Copy the file to the specified directory
            import shutil
            shutil.copy(file_path, new_file_path)
            data_file_path = new_file_path  # Save the new file path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file to the directory:\n{e}")
            return

        # Read and display the CSV content
        data = pd.read_csv(new_file_path)
        tree.delete(*tree.get_children())  # Clear previous content
        tree["columns"] = list(data.columns)
        tree["show"] = "headings"
        for column in data.columns:
            tree.heading(column, text=column)
            tree.column(column, width=100)
        for _, row in data.iterrows():
            tree.insert("", "end", values=list(row))
        messagebox.showinfo("File Uploaded", f"File successfully uploaded!\nStored at: {new_file_path}")
    else:
        messagebox.showwarning("No File", "No file was selected.")

def apply_rules_and_profile():
    messagebox.showwarning("Data profiling", "rules.csv rules are applied data.csv")
    genRegex.mycall()

def open_admin_home():
    """Create Admin Home UI."""
    admin_home = tk.Tk()
    admin_home.title("Admin Home")
    admin_home.geometry("800x600")
    # Buttons
    button_frame = tk.Frame(admin_home)
    button_frame.pack(side="bottom", fill="x", pady=10)

    tk.Button(button_frame, text="Upload Rules", command=lambda: upload_csv(tree1)).pack(side="left", padx=5)
    tk.Button(button_frame, text="Upload Data", command=lambda: upload_csv(tree2)).pack(side="left", padx=5)
    tk.Button(button_frame, text="Apply Rules & Profile", command=apply_rules_and_profile).pack(side="left", padx=5)
    tk.Button(button_frame, text="Logout", command=admin_home.destroy).pack(side="right", padx=5)

    # Treeviews for rules and data
    tree1 = ttk.Treeview(admin_home)
    tree1.pack(expand=True, fill="both", pady=10)
    tree2 = ttk.Treeview(admin_home)
    tree2.pack(expand=True, fill="both", pady=10)


    admin_home.mainloop()

def login():
    """Handle login and redirect."""
    username = username_entry.get()
    password = password_entry.get()
    role = role_var.get()

    if role == "Admin" and username == "admin" and password == "admin123":
        login_window.destroy()
        open_admin_home()
    elif role == "User" and username == "user" and password == "user123":
        messagebox.showinfo("User Login", "User role is currently under development!")
    else:
        messagebox.showerror("Login Failed", "Invalid credentials!")

# Login UI
login_window = tk.Tk()
login_window.title("Gen AI-Based Data Profiling")
login_window.geometry("800x600")

# Input Frame
input_frame = tk.Frame(login_window)
input_frame.pack(pady=20)

tk.Label(input_frame, text="Username:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
username_entry = tk.Entry(input_frame)
username_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Password:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
password_entry = tk.Entry(input_frame, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(input_frame, text="Role:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
role_var = tk.StringVar(value="Admin")
tk.Radiobutton(input_frame, text="Admin", variable=role_var, value="Admin").grid(row=2, column=1, sticky="w")
tk.Radiobutton(input_frame, text="User", variable=role_var, value="User").grid(row=2, column=2, sticky="w")

tk.Button(input_frame, text="Login", command=login).grid(row=3, column=0, columnspan=2, pady=20)

login_window.mainloop()
