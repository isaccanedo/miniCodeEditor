import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import subprocess
import jedi

THEMES = {
    "dark": {
        "bg": "#1E1E1E",
        "fg": "#D4D4D4",
        "text_bg": "#252526",
        "text_fg": "#D4D4D4",
        "console_bg": "#1E1E1E",
        "console_fg": "#D4D4D4",
        "button_bg": "#007ACC",
        "button_fg": "white",
        "btn_cls": "#b81414"
    },
    "light": {
        "bg": "#FFFFFF",
        "fg": "#000000",
        "text_bg": "#F0F0F0",
        "text_fg": "#000000",
        "console_bg": "#FFFFFF",
        "console_fg": "#000000",
        "button_bg": "#007ACC",
        "button_fg": "white"
    }
}

current_theme = "dark"

def toggle_theme():
    global current_theme
    current_theme = "light" if current_theme == "dark" else "dark"
    apply_theme()

def apply_theme():
    theme = THEMES[current_theme]
    root.config(bg=theme["bg"])
    text_editor.config(bg=theme["text_bg"], fg=theme["text_fg"], insertbackground=theme["fg"])
    console_output.config(bg=theme["console_bg"], fg=theme["console_fg"])
    lang_menu.config(bg=theme["button_bg"], fg=theme["button_fg"])
    save_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
    clear_button.config(bg=theme["btn_cls"], fg=theme["button_fg"])
    run_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
    theme_button.config(bg=theme["button_bg"], fg=theme["button_fg"])

# code execution
def run_code():
    code = text_editor.get("1.0", tk.END).strip()
    language = lang_var.get()

    if not code:
        messagebox.showwarning("Warning", "The code is empty.")
        return

    file_ext = "py" if language == "Python" else "js"
    file_name = f"temp_script.{file_ext}"
    cmd = ["python", file_name] if language == "Python" else ["node", file_name]

    try:
        # save code in file 
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(code)
        result = subprocess.run(cmd, capture_output=True, text=True)

        # show result in console
        console_output.config(state=tk.NORMAL)
        console_output.delete("1.0", tk.END)
        console_output.insert(tk.END, result.stdout if result.stdout else result.stderr)
        console_output.config(state=tk.DISABLED)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# save function
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Python Files", "*.py"),
                                                        ("JavaScript Files", "*.js"),
                                                        ("Text Files", "*.txt"),
                                                        ("All Files", "*.*")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(text_editor.get("1.0", tk.END).strip())
            messagebox.showinfo("Success", "File saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file:\n{e}")

def clear_editor():
    text_editor.delete("1.0", tk.END)

# autocomplete function in progress...
def autocomplete(event):
    code = text_editor.get("1.0", tk.END)
    cursor_pos = text_editor.index(tk.INSERT)

    script = jedi.Script(code, path="temp.py")
    try:
        completions = script.complete(*map(int, cursor_pos.split(".")))
        if completions:
            text_editor.insert(tk.INSERT, completions[0].name[len(event.char):])
            text_editor.mark_set(tk.INSERT, cursor_pos)
    except Exception:
        pass

root = tk.Tk()
root.title("Mini Code Editor")
root.geometry("900x600")
root.configure(bg="#1e1e1e")

frame_top = tk.Frame(root)
frame_top.pack(pady=5, fill=tk.X)
frame = tk.Frame(root, bg="#252526")

save_button = tk.Button(frame_top, text="Save", command=save_file)
save_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(frame_top, text="Clear", command=clear_editor)
clear_button.pack(side=tk.LEFT, padx=5)

lang_var = tk.StringVar(value="Python")
lang_menu = tk.OptionMenu(frame_top, lang_var, "Python", "JavaScript")
lang_menu.pack(side=tk.LEFT, padx=5)

run_button = tk.Button(frame_top, text="Run", command=run_code)
run_button.pack(side=tk.RIGHT, padx=5)

theme_button = tk.Button(frame_top, text="Toggle Theme", command=toggle_theme)
theme_button.pack(side=tk.RIGHT, padx=5)

text_editor = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Courier", 12), height=20)
text_editor.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

console_label = tk.Label(root, text="Console Output", font=("Arial", 10, "bold"))
console_label.pack(pady=5)

console_output = scrolledtext.ScrolledText(root, height=8, wrap=tk.WORD, font=("Courier", 10), state=tk.DISABLED)
console_output.pack(padx=10, pady=5, fill=tk.BOTH, expand=False)

apply_theme()

root.mainloop()
