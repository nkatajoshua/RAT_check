import os
import tkinter as tk
from tkinter import filedialog, messagebox
import concurrent.futures

def search_for_rat_indicators(file_path):
    rat_indicators = [
        "reverse_shell",
        "backdoor",
        "remote_access_trojan",
        "rat_payload",
        # Add more indicators as needed
    ]

    try:
        with open(file_path, "r", errors="ignore") as file:
            content = file.read().lower()

            if any(indicator in content for indicator in rat_indicators):
                return True
    except:
        pass

    return False

def scan_directory(directory):
    potential_rats = []

    for root, _, files in os.walk(directory):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_file = {executor.submit(search_for_rat_indicators, os.path.join(root, file)): file for file in files}
            for future in concurrent.futures.as_completed(future_to_file):
                file = future_to_file[future]
                if future.result():
                    potential_rats.append(file)

    return potential_rats

def browse_directory():
    selected_directory = filedialog.askdirectory()
    if selected_directory:
        potential_rats = scan_directory(selected_directory)
        if potential_rats:
            result_message = "\n".join(potential_rats)
            messagebox.showwarning("Potential RATs Found", f"The following files might contain potential RATs:\n\n{result_message}")
        else:
            messagebox.showinfo("No Potential RATs", "No potential RATs were found in the selected directory.")

def main():
    app = tk.Tk()
    app.title("RAT Check App")
    app.geometry("400x200")

    label = tk.Label(app, text="Select a directory to scan for potential RATs:")
    label.pack(pady=10)

    browse_button = tk.Button(app, text="Browse", command=browse_directory)
    browse_button.pack(pady=20)

    app.mainloop()

if __name__ == "__main__":
    main()
