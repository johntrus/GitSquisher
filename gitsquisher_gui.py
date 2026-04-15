import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
from repo_status import get_repo_status
from git_structure import build_interactive_structure
from gitignore_manager import add_to_gitignore, remove_from_gitignore
from squisher import create_squish, list_squishable_files
from squisher_encrypt import encrypt_squish
from squisher_decrypt import decrypt_latest_squish
from squisher_shutdown import safe_shutdown
from squisher_style import SquisherStyle
from squisher_layout import create_widgets

class GitSquisherGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GitSquisher - Project Zipper & AI Assistant")
        
        self.style = SquisherStyle()
        self.root.configure(bg=self.style.bg_color)
        
        # Responsive window: 70vw x 90vh, centered, with minimum size
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        width = int(screen_w * 0.70)
        height = int(screen_h * 0.90)
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(800, 600)
        
        self.path_var = tk.StringVar()
        self.project_name_var = tk.StringVar()
        
        # Delegate full widget creation + layout to squisher_layout.py
        create_widgets(self)
        
    def browse(self):
        dir_path = filedialog.askdirectory(title="Select Project Root Directory")
        if dir_path:
            self.path_var.set(dir_path)
            self.load_repository()  # Auto-load on browse for better UX
            
    def load_repository(self):
        path = self.path_var.get().strip()
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)
        
        if not path:
            self.status_text.insert(tk.END, "❌ Please select or enter a directory path.\n", "error")
            self.status_text.config(state="disabled")
            self.preview_label.config(text="📦 0 clean files will be squished")
            return
        
        status_data = get_repo_status(path, self.project_name_var.get().strip())
        self.project_name_var.set(status_data["project_name"])
        
        for text, tag in status_data.get("status_lines", []):
            self.status_text.insert(tk.END, text, tag)
        
        self.status_text.config(state="disabled")
        self._populate_structure(path)
        
        files_to_squish = list_squishable_files(path)
        self.preview_label.config(
            text=f"📦 {len(files_to_squish)} clean files will be squished"
        )
        
    def _populate_structure(self, root_path: str):
        """Build two-column rows using the modular helper."""
        for widget in self.structure_inner.winfo_children():
            widget.destroy()
        
        try:
            rows = build_interactive_structure(root_path)
            for idx, row_data in enumerate(rows):
                frame = tk.Frame(self.structure_inner, bg=self.style.panel_color)
                frame.grid(row=idx, column=0, sticky="ew", padx=10, pady=4 if row_data["type"] == "dir" else 2)
                
                tk.Label(frame, text=f"{row_data['indent']}{row_data['display_name']}", 
                         bg=self.style.panel_color, fg=row_data["fg_color"], font=("Consolas", 11)).pack(side=tk.LEFT)
                
                if row_data["button_text"]:
                    btn_text = row_data["button_text"]
                    btn_fg = row_data["button_fg"]
                    rel_path = row_data["rel_path"]
                    is_ignored = row_data["is_ignored"]
                    btn_cmd = lambda p=rel_path, r=root_path, ign=is_ignored: self._remove_from_gitignore(p, r) if ign else self._add_to_gitignore(p, r)
                    tk.Button(frame, text=btn_text, fg=btn_fg, 
                              bg=self.style.panel_color, font=("Helvetica", 14, "bold"), relief="flat", width=3,
                              command=btn_cmd).pack(side=tk.RIGHT, padx=10)
        except Exception as e:
            tk.Label(self.structure_inner, text=f"❌ Could not read structure: {e}", 
                     bg=self.style.panel_color, fg=self.style.error_color).grid(row=0, column=0, sticky="w", padx=10)
        
    def _add_to_gitignore(self, rel_path: str, root_path: str):
        add_to_gitignore(rel_path, root_path)
        self.load_repository()
        
    def _remove_from_gitignore(self, rel_path: str, root_path: str):
        remove_from_gitignore(rel_path, root_path)
        self.load_repository()
        
    def squish_project(self):
        path = self.path_var.get().strip()
        if not path:
            messagebox.showerror("Error", "Please load a project directory first.")
            return
        
        project_name = self.project_name_var.get().strip() or os.path.basename(path)
        
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, "\n🗜️ Starting Squish (Zip)...\n", "info")
        self.status_text.see(tk.END)
        self.root.update()
        
        success, msg = create_squish(path, project_name)
        
        if success:
            self.status_text.insert(tk.END, f"{msg}\n", "success")
        else:
            self.status_text.insert(tk.END, f"{msg}\n", "error")
        
        self.status_text.config(state="disabled")
        self.load_repository()
     
    def show_help(self):
        """Show friendly help popup with quick start and tips."""
        help_text = """GitSquisher Help 🗜️🍇

Quick Start:
1. Browse → pick your project folder
2. Click "Load Repository" (or it auto-loads)
3. See live Git status + ignore toggles
4. Click "Squish Project" → clean zip
5. Click "Encrypt & Key" → AES-256 + auto key rotation
6. Click "Decrypt Latest" when you get it back

Pro tips:
• .gitignore is fully respected (and editable live)
• Keys rotate every 90 days automatically
• Your encryption key is auto-added to .gitignore
• Works perfectly with Cursor, Claude, Grok, Windsurf, etc.

Enjoy the squish! 🔥

           Made with ❤️ by @johntrus
"""
        messagebox.showinfo("GitSquisher Help", help_text)
   
    def encrypt_project(self):
        path = self.path_var.get().strip()
        if not path:
            messagebox.showerror("Error", "Please load a project directory first.")
            return
        
        project_name = self.project_name_var.get().strip() or os.path.basename(path)
        
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, "\n🔐 Starting Encrypt & Key...\n", "info")
        self.status_text.see(tk.END)
        self.root.update()
        
        success, msg = encrypt_squish(path, project_name)
        
        if success:
            self.status_text.insert(tk.END, f"{msg}\n", "success")
        else:
            self.status_text.insert(tk.END, f"{msg}\n", "error")
        
        self.status_text.config(state="disabled")
        self.load_repository()
        
    def decrypt_project(self):
        """One-click decrypt of the latest encrypted squish using automated key-rotation support."""
        path = self.path_var.get().strip()
        if not path:
            messagebox.showerror("Error", "Please load a project directory first.")
            return
        
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, "\n🔓 Starting Decrypt Latest...\n", "info")
        self.status_text.see(tk.END)
        self.root.update()
        
        success, msg = decrypt_latest_squish(path)
        
        if success:
            self.status_text.insert(tk.END, f"{msg}\n", "success")
        else:
            self.status_text.insert(tk.END, f"{msg}\n", "error")
        
        self.status_text.config(state="disabled")
        self.load_repository()
        
    def exit_app(self):
        safe_shutdown(self.root)

if __name__ == "__main__":
    app = GitSquisherGUI()
    app.root.mainloop()
