import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
from repo_status import get_repo_status
from git_structure import build_interactive_structure
from ignore_template import apply_ignore_template, clear_ignore_list
from gitignore_manager import add_to_gitignore, remove_from_gitignore

class GitSquisherGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GitSquisher - Project Zipper & AI Assistant")
        
        # Refined night-time color scheme with deeper contrast and modern polish
        self.bg_color = "#0a0a14"
        self.panel_color = "#141425"
        self.fg_color = "#c3c8ff"
        self.accent_color = "#8b5cf6"
        self.success_color = "#22c55e"
        self.warning_color = "#eab308"
        self.error_color = "#ef4444"
        self.grey_color = "#9ca3af"
        
        self.root.configure(bg=self.bg_color)
        
        # Responsive window: 70vw x 90vh, perfectly centered, with generous minimum size
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        width = int(screen_w * 0.70)
        height = int(screen_h * 0.90)
        x = (screen_w - width) // 2
        y = (screen_h - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.minsize(880, 620)
        
        self.path_var = tk.StringVar()
        self.project_name_var = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container with two columns (left controls, right content)
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)
        
        # LEFT: Controls panel
        left = tk.Frame(main_frame, bg=self.panel_color, width=440)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        left.grid_propagate(False)
        
        tk.Label(left, text="GitSquisher", font=("Helvetica", 32, "bold"), 
                 bg=self.panel_color, fg=self.accent_color).pack(pady=(0, 28))
        
        # Project Directory
        tk.Label(left, text="Project Directory", font=("Helvetica", 14, "bold"), 
                 bg=self.panel_color, fg=self.fg_color).pack(anchor="w", padx=28, pady=(0, 6))
        entry = tk.Entry(left, textvariable=self.path_var, font=("Consolas", 13), 
                        bg="#1f1f2e", fg=self.fg_color, relief="flat", bd=0, 
                        highlightthickness=2, highlightbackground=self.accent_color, 
                        highlightcolor=self.accent_color, insertbackground=self.fg_color)
        entry.pack(fill=tk.X, padx=28, pady=(0, 12), ipady=10)
        
        btn_frame = tk.Frame(left, bg=self.panel_color)
        btn_frame.pack(pady=10, padx=28, fill=tk.X)
        
        tk.Button(btn_frame, text="Browse Folder", command=self.browse, 
                  bg=self.accent_color, fg="white", font=("Helvetica", 12, "bold"), 
                  relief="flat", height=2, activebackground="#a78bfa", 
                  highlightthickness=0).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Button(btn_frame, text="Load Repo", command=self.load_repository, 
                  bg=self.success_color, fg="white", font=("Helvetica", 12, "bold"), 
                  relief="flat", height=2, activebackground="#4ade80", 
                  highlightthickness=0).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Project Name
        tk.Label(left, text="Project Name", font=("Helvetica", 14, "bold"), 
                 bg=self.panel_color, fg=self.fg_color).pack(anchor="w", padx=28, pady=(24, 6))
        project_entry = tk.Entry(left, textvariable=self.project_name_var, font=("Consolas", 13), 
                        bg="#1f1f2e", fg=self.fg_color, relief="flat", bd=0, 
                        highlightthickness=2, highlightbackground=self.accent_color, 
                        highlightcolor=self.accent_color, insertbackground=self.fg_color)
        project_entry.pack(fill=tk.X, padx=28, pady=(0, 12), ipady=10)
        
        # Ignore Management
        tk.Label(left, text="Ignore Management", font=("Helvetica", 14, "bold"), 
                 bg=self.panel_color, fg=self.fg_color).pack(anchor="w", padx=28, pady=(28, 8))
        
        ignore_btn_frame = tk.Frame(left, bg=self.panel_color)
        ignore_btn_frame.pack(pady=8, padx=28, fill=tk.X)
        
        tk.Button(ignore_btn_frame, text="Use Ignore Template", command=self.use_ignore_template, 
                  bg=self.warning_color, fg="white", font=("Helvetica", 12, "bold"), 
                  relief="flat", height=2, activebackground="#facc15", 
                  highlightthickness=0).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        tk.Button(ignore_btn_frame, text="Clear Ignore List", command=self.clear_ignore_list, 
                  bg=self.error_color, fg="white", font=("Helvetica", 12, "bold"), 
                  relief="flat", height=2, activebackground="#f87171", 
                  highlightthickness=0).pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # RIGHT: Content area
        right = tk.Frame(main_frame, bg=self.panel_color)
        right.grid(row=0, column=1, sticky="nsew")
        
        # Repository Status (compact)
        header_frame = tk.Frame(right, bg=self.panel_color)
        header_frame.pack(fill=tk.X, padx=24, pady=(20, 6))
        
        tk.Label(header_frame, text="Repository Status", font=("Helvetica", 17, "bold"), 
                 bg=self.panel_color, fg=self.fg_color).pack(side=tk.LEFT)
        
        tk.Button(header_frame, text="Refresh", command=self.load_repository, 
                  bg=self.panel_color, fg=self.accent_color, font=("Helvetica", 10, "bold"), 
                  relief="flat", activebackground="#1f1f2e").pack(side=tk.RIGHT)
        
        self.status_text = tk.Text(right, bg="#1a1a2b", fg="#a5b4fc", font=("Consolas", 12.5),
                                  relief="flat", padx=20, pady=14, wrap=tk.WORD, state="disabled", height=7)
        self.status_text.pack(fill=tk.BOTH, expand=False, padx=24, pady=(0, 12))
        
        status_scrollbar = ttk.Scrollbar(right, command=self.status_text.yview)
        status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 12))
        self.status_text.config(yscrollcommand=status_scrollbar.set)
        
        self.status_text.tag_config("success", foreground=self.success_color)
        self.status_text.tag_config("warning", foreground=self.warning_color)
        self.status_text.tag_config("error", foreground=self.error_color)
        self.status_text.tag_config("info", foreground=self.fg_color)
        
        # Interactive Project Structure (expanded)
        structure_header = tk.Frame(right, bg=self.panel_color)
        structure_header.pack(fill=tk.X, padx=24, pady=(16, 8))
        
        tk.Label(structure_header, text="Project Structure", font=("Helvetica", 17, "bold"), 
                 bg=self.panel_color, fg=self.fg_color).pack(side=tk.LEFT)
        
        self.structure_canvas = tk.Canvas(right, bg="#1a1a2b", highlightthickness=0)
        self.structure_canvas.pack(fill=tk.BOTH, expand=True, padx=24, pady=(0, 20))
        
        structure_scrollbar = ttk.Scrollbar(right, orient="vertical", command=self.structure_canvas.yview)
        structure_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 20))
        self.structure_canvas.configure(yscrollcommand=structure_scrollbar.set)
        
        self.structure_inner = tk.Frame(self.structure_canvas, bg="#1a1a2b")
        self.structure_canvas.create_window((0, 0), window=self.structure_inner, anchor="nw")
        
        self.structure_inner.bind("<Configure>", 
                                  lambda e: self.structure_canvas.configure(scrollregion=self.structure_canvas.bbox("all")))
        
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
    def browse(self):
        dir_path = filedialog.askdirectory(title="Select Project Root Directory")
        if dir_path:
            self.path_var.set(dir_path)
            self.load_repository()
            
    def load_repository(self):
        path = self.path_var.get().strip()
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)
        
        if not path:
            self.status_text.insert(tk.END, "❌ Please select or enter a directory path.\n", "error")
            self.status_text.config(state="disabled")
            return
        
        status_data = get_repo_status(path, self.project_name_var.get().strip())
        self.project_name_var.set(status_data["project_name"])
        
        for text, tag in status_data.get("status_lines", []):
            self.status_text.insert(tk.END, text, tag)
        
        self.status_text.config(state="disabled")
        self._populate_structure(path)
        
    def _populate_structure(self, root_path: str):
        """Delegate entire structure rendering to the dedicated helper (no duplication)."""
        for widget in self.structure_inner.winfo_children():
            widget.destroy()
        
        rows = build_interactive_structure(root_path)
        row = 0
        
        for item in rows:
            if item["type"] in ("dir", "file"):
                frame = tk.Frame(self.structure_inner, bg="#1a1a2b")
                frame.grid(row=row, column=0, sticky="ew", padx=12, pady=3 if item["type"] == "file" else 5)
                
                # Column 1: name
                tk.Label(frame, text=f"{item['indent']}{item['display_name']}", 
                         bg="#1a1a2b", fg=item["fg_color"], font=("Consolas", 12)).pack(side=tk.LEFT, padx=(0, 8))
                
                # Column 2: dynamic button
                if item["button_text"]:
                    tk.Button(frame, text=item["button_text"], fg=item["button_fg"], 
                              bg="#1a1a2b", font=("Helvetica", 15, "bold"), relief="flat", width=3,
                              command=lambda p=item["rel_path"], r=root_path: 
                              self.remove_from_gitignore(p, r) if item["is_ignored"] else self.add_to_gitignore(p, r)
                              ).pack(side=tk.RIGHT, padx=8)
                row += 1
                
            elif item["type"] == "info":
                tk.Label(self.structure_inner, text=item["display_name"], 
                         bg="#1a1a2b", fg="#a5b4fc", font=("Consolas", 11)).grid(row=row, column=0, sticky="w", padx=12)
                row += 1
            elif item["type"] == "error":
                tk.Label(self.structure_inner, text=item["display_name"], 
                         bg="#1a1a2b", fg="#ef4444").grid(row=row, column=0, sticky="w", padx=12)
                row += 1
        
    def add_to_gitignore(self, rel_path: str, root_path: str):
        success, msg = add_to_gitignore(rel_path, root_path)
        if success:
            self.load_repository()
        else:
            print(msg)
        
    def remove_from_gitignore(self, rel_path: str, root_path: str):
        success, msg = remove_from_gitignore(rel_path, root_path)
        if success:
            self.load_repository()
        else:
            print(msg)
            
    def use_ignore_template(self):
        path = self.path_var.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "Please load a valid project directory first.")
            return
        if messagebox.askyesno("Confirm Template", 
                               "Do you understand that you are about to use a template?\n\n"
                               "This will add the standard GitSquisher .gitignore while preserving your existing custom entries."):
            name = self.project_name_var.get().strip()
            success, msg = apply_ignore_template(path, name)
            if success:
                messagebox.showinfo("Success", msg)
                self.load_repository()
            else:
                messagebox.showerror("Error", msg)
    
    def clear_ignore_list(self):
        path = self.path_var.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showerror("Error", "Please load a valid project directory first.")
            return
        if messagebox.askyesno("Confirm Reset", 
                               "This will completely reset your .gitignore.\n\n"
                               "Are you sure?"):
            success, msg = clear_ignore_list(path)
            if success:
                messagebox.showinfo("Success", msg)
                self.load_repository()
            else:
                messagebox.showerror("Error", msg)

if __name__ == "__main__":
    app = GitSquisherGUI()
    app.root.mainloop()
