import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math
import json
import os

def get_diff_name(stars: float) -> str:
    if 0.0 <= stars <= 1.99:
        return "Easy"
    elif 2.0 <= stars <= 2.69:
        return "Normal"
    elif 2.7 <= stars <= 3.99:
        return "Hard"
    elif 4.0 <= stars <= 5.29:
        return "Insane"
    elif 5.3 <= stars <= 6.49:
        return "Expert"
    elif stars >= 6.5:
        return "Expert+"
    else:
        return "Unknown"

def load_beatmaps(file_path):
    """Load beatmaps from JSON file"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return []
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load beatmaps: {e}")
        return []

def sort_beatmaps_by_bracket(beatmaps):
    """Sort beatmaps by bracket in the correct order"""
    bracket_order = ["normal", "hard", "insane", "expert", "expert+", "expert++"]
    
    def get_bracket_sort_key(beatmap):
        bracket = beatmap["bracket"].lower()
        if bracket in bracket_order:
            return bracket_order.index(bracket)
        return len(bracket_order)  # Put unknown brackets at the end
    
    return sorted(beatmaps, key=get_bracket_sort_key)

def save_beatmaps(file_path, beatmaps):
    """Save beatmaps to JSON file with automatic sorting"""
    try:
        # Sort beatmaps before saving
        sorted_beatmaps = sort_beatmaps_by_bracket(beatmaps)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_beatmaps, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save beatmaps: {e}")
        return False

def add_beatmap_to_json():
    """Add current beatmap to beatmaps.json"""
    title = title_entry.get().strip()
    artist = artist_entry.get().strip()
    bracket = mode_var.get()
    length = length_entry.get().strip()
    
    # Validation
    if not title or not artist or not bracket or not length:
        messagebox.showerror("Error", "Please fill in all fields")
        return
    
    if bracket == "Select...":
        messagebox.showerror("Error", "Please select a bracket")
        return
    
    try:
        stars = float(stars_entry.get())
        if stars < 0:
            raise ValueError("Stars must be positive")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid star rating")
        return
    
    # Create beatmap entry
    diff_name = get_diff_name(stars)
    diff_formatted = f"{diff_name} ({stars:.2f}★)"
    
    new_beatmap = {
        "title": title,
        "artist": artist,
        "bracket": bracket,
        "diff": diff_formatted,
        "length": length
    }
    
    # Load existing beatmaps
    beatmaps = load_beatmaps("beatmaps.json")
    
    # Add new beatmap
    beatmaps.append(new_beatmap)
    
    # Save updated beatmaps
    if save_beatmaps("beatmaps.json", beatmaps):
        messagebox.showinfo("Success", f"Added '{title}' to beatmaps.json")
        # Clear form
        title_entry.delete(0, tk.END)
        artist_entry.delete(0, tk.END)
        stars_entry.delete(0, tk.END)
        length_entry.delete(0, tk.END)
        mode_var.set("Select...")
    else:
        messagebox.showerror("Error", "Failed to save beatmap")

def load_and_display_json():
    """Load beatmaps.json and display in text widget with automatic sorting"""
    file_path = filedialog.askopenfilename(
        title="Select beatmaps.json file",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    
    if file_path:
        beatmaps = load_beatmaps(file_path)
        if beatmaps:
            # Sort beatmaps before displaying
            sorted_beatmaps = sort_beatmaps_by_bracket(beatmaps)
            # Display formatted JSON in output text
            formatted_json = json.dumps(sorted_beatmaps, indent=2, ensure_ascii=False)
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, formatted_json)
            messagebox.showinfo("Success", f"Loaded and sorted {len(beatmaps)} beatmaps")

def save_current_as_json():
    """Save current beatmaps.json to a new file with automatic sorting"""
    beatmaps = load_beatmaps("beatmaps.json")
    if not beatmaps:
        messagebox.showwarning("Warning", "No beatmaps found in beatmaps.json")
        return
    
    file_path = filedialog.asksaveasfilename(
        title="Save beatmaps as...",
        defaultextension=".json",
        filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    )
    
    if file_path:
        if save_beatmaps(file_path, beatmaps):
            messagebox.showinfo("Success", f"Saved and sorted {len(beatmaps)} beatmaps to {file_path}")

def format_song():
    title = title_entry.get()
    artist = artist_entry.get()
    mode = mode_var.get()
    length = length_entry.get()
    
    try:
        stars = float(stars_entry.get())
        diff_name = get_diff_name(stars)
        diff_formatted = f"{diff_name} ({stars:.2f}★)"
    except ValueError:
        diff_formatted = "Invalid stars"
    
    formatted = f'{{ title: "{title}", artist: "{artist}", bracket: "{mode}", diff: "{diff_formatted}", length: "{length}" }},'
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, formatted)

def format_scaled_score(score):
    """Format scaled score with apostrophe separators"""
    scaled_score = int(score)
    return f"{scaled_score:,}".replace(",", "'")

def calculate_score():
    try:
        acc = float(acc_entry.get())
        combo = int(combo_entry.get())
        max_combo = int(max_combo_entry.get())
        
        # Base formula
        score = ((0.8 * acc) * 100) + ((0.2 * math.sqrt(combo / max_combo)) * 100)
        
        # Apply mod multiplier
        mod = mod_var.get()
        multipliers = {
            "None": 1.0,
            "Easy (EZ)": 0.50,
            "Hard Rock (HR)": 1.12,
            "Hidden (HD)": 1.05,
            "Flashlight (FL)": 1.10
        }
        score *= multipliers.get(mod, 1.0)
        
        # Calculate scaled score (8020 = 1,000,000 ratio)
        scaled_score = (score / 8020.0) * 1000000
        formatted_scaled = format_scaled_score(scaled_score)
        
        score_output.config(text=f"Score: {score:.2f} | Scaled: {formatted_scaled}")
    except Exception as e:
        score_output.config(text=f"Error: {e}")

# Main window
root = tk.Tk()
root.title("osu! Formatter & Score Calculator")

# --- Section 1: Song Formatter ---
formatter_frame = ttk.LabelFrame(root, text="Song Formatter")
formatter_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(formatter_frame, text="Title:").grid(row=0, column=0, sticky="w")
title_entry = ttk.Entry(formatter_frame, width=30)
title_entry.grid(row=0, column=1)

ttk.Label(formatter_frame, text="Artist:").grid(row=1, column=0, sticky="w")
artist_entry = ttk.Entry(formatter_frame, width=30)
artist_entry.grid(row=1, column=1)

ttk.Label(formatter_frame, text="Bracket:").grid(row=2, column=0, sticky="w")
mode_var = tk.StringVar(value="Select...")
mode_menu = ttk.Combobox(formatter_frame, textvariable=mode_var, values=["normal", "hard", "insane", "expert", "expert+", "expert++"], state="readonly")
mode_menu.grid(row=2, column=1)

ttk.Label(formatter_frame, text="Stars:").grid(row=3, column=0, sticky="w")
stars_entry = ttk.Entry(formatter_frame, width=30)
stars_entry.grid(row=3, column=1)

ttk.Label(formatter_frame, text="Length:").grid(row=4, column=0, sticky="w")
length_entry = ttk.Entry(formatter_frame, width=30)
length_entry.grid(row=4, column=1)

format_button = ttk.Button(formatter_frame, text="Format", command=format_song)
format_button.grid(row=5, column=0, pady=5)

add_button = ttk.Button(formatter_frame, text="Add to beatmaps.json", command=add_beatmap_to_json)
add_button.grid(row=5, column=1, pady=5)

# JSON management buttons
json_frame = ttk.Frame(formatter_frame)
json_frame.grid(row=6, column=0, columnspan=2, pady=5)

load_button = ttk.Button(json_frame, text="Load JSON", command=load_and_display_json)
load_button.pack(side="left", padx=5)

save_button = ttk.Button(json_frame, text="Save As...", command=save_current_as_json)
save_button.pack(side="left", padx=5)

output_text = tk.Text(formatter_frame, height=8, width=60)
output_text.grid(row=7, column=0, columnspan=2, pady=5)

# --- Section 2: Score Calculator ---
score_frame = ttk.LabelFrame(root, text="Score Calculator")
score_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(score_frame, text="Accuracy (to 4SF):").grid(row=0, column=0, sticky="w")
acc_entry = ttk.Entry(score_frame, width=15)
acc_entry.grid(row=0, column=1)

ttk.Label(score_frame, text="Combo:").grid(row=1, column=0, sticky="w")
combo_entry = ttk.Entry(score_frame, width=15)
combo_entry.grid(row=1, column=1)

ttk.Label(score_frame, text="Max Combo:").grid(row=2, column=0, sticky="w")
max_combo_entry = ttk.Entry(score_frame, width=15)
max_combo_entry.grid(row=2, column=1)

ttk.Label(score_frame, text="Mod:").grid(row=3, column=0, sticky="w")
mod_var = tk.StringVar(value="None")
mod_menu = ttk.Combobox(score_frame, textvariable=mod_var, values=["None", "Easy (EZ)", "Hard Rock (HR)", "Hidden (HD)", "Flashlight (FL)"], state="readonly")
mod_menu.grid(row=3, column=1)

calc_button = ttk.Button(score_frame, text="Calculate Score", command=calculate_score)
calc_button.grid(row=4, column=0, columnspan=2, pady=5)

score_output = ttk.Label(score_frame, text="Score: ")
score_output.grid(row=5, column=0, columnspan=2)

root.mainloop()
