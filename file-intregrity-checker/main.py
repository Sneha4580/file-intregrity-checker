import os
import hashlib
import json
import tkinter as tk
from tkinter import messagebox

# === SETTINGS ===
FOLDER = "test_files"          # Folder to scan
HASH_FILE = "hash_store.json" # Where hashes are saved


# === FUNCTION: Create SHA-256 hash of a file ===
def get_file_hash(filename):
    hasher = hashlib.sha256()
    with open(filename, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


# === FUNCTION: Save current hashes to file ===
def scan_files():
    hashes = {}
    for root, dirs, files in os.walk(FOLDER):
        for name in files:
            path = os.path.join(root, name)
            rel_path = os.path.relpath(path, FOLDER)
            hashes[rel_path] = get_file_hash(path)
    with open(HASH_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)
    print("✅ File hashes saved!")


# === FUNCTION: Check if any file has changed ===
def check_integrity():
    try:
        with open(HASH_FILE, 'r') as f:
            old_hashes = json.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "No hash file found. Please scan files first.")
        return

    changed = []
    for root, dirs, files in os.walk(FOLDER):
        for name in files:
            path = os.path.join(root, name)
            rel_path = os.path.relpath(path, FOLDER)
            current_hash = get_file_hash(path)
            old_hash = old_hashes.get(rel_path)

            if old_hash is None:
                changed.append(f"🆕 New file: {rel_path}")
            elif current_hash != old_hash:
                changed.append(f"⚠️ Modified: {rel_path}")

    if changed:
        changes_text = "\n".join(changed)
        messagebox.showwarning("Changes Found", changes_text)
    else:
        messagebox.showinfo("All Good", "✅ All files are OK!")


# === GUI Wrappers for Buttons ===
def gui_scan():
    scan_files()
    messagebox.showinfo("Done", "File hashes saved successfully.")


def gui_check():
    check_integrity()


# === GUI Setup ===
root = tk.Tk()
root.title("File Integrity Checker")
root.geometry("300x200")

title_label = tk.Label(root, text="File Integrity Checker", font=("Arial", 14))
title_label.pack(pady=10)

btn_scan = tk.Button(root, text="🔍 Scan Files", command=gui_scan, height=2, width=25)
btn_scan.pack(pady=10)

btn_check = tk.Button(root, text="✅ Check Integrity", command=gui_check, height=2, width=25)
btn_check.pack(pady=5)

footer_label = tk.Label(root, text="Folder: test_files", font=("Arial", 9), fg="gray")
footer_label.pack(pady=10)

root.mainloop()
