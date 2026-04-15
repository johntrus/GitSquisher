import tkinter as tk
from tkinter import filedialog, ttk
import os
import subprocess
from repo_status import get_repo_status

class GitSquisherGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GitSquisher - Project Zipper & AI Assistant")
        
        # Night time color scheme (refined for deeper contrast and modern feel)
        self.bg_color = "#0a0a14"
        self.panel_color = "#141425"
        self.fg_color = "#c3c8ff"
        self.accent_color = "#8b5cf6"
        self.success_color = "#22c55e"
        self.warning_color = "#eab308"
        self.error_color = "#ef4444"
        self.grey_color = "#9ca3af"  # for ignored items
        
        self.root.configure(bg=self.bg_color)
        
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
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container with two columns using grid for better responsiveness
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # LEFT: Controls panel
        left = tk.Frame(main_frame, bg=self.panel_color, width=420)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        left.grid_propagate(False)
        
        tk.Label(left, text="GitSquisher", font=("Helvetica", 28, "bold"), 
                 bg=self.panel_color, fg=self.accent_color).pack(pady=25)
        
        tk.Label(left, text="Project Directory", font=("Helvetica", 14, "bold"), 
                 bg=self.panel_color, fg=self.fg_color).pack(anchor="w", padx=25, pady=(0, 8))
        
        entry = tk.Entry(left, textvariable=self.path_var, font=("Consolas", 12), 
                        bg="#1f1f2e", fg=self.fg_color, relief="flat", bd=0, 
                        highlightthickness=2, highlightbackground=self.accent_color, 
                        highlightcolor=self.accent_color, insertbackground=self.fg_color)
        entry.pack(fill=tk.X, padx=25, pady=8, ipady=8)
        
        btn_frame = tk.Frame(left, bg=self.panel_color)
        btn_frame.pack(pady=12, padx=25, fill=tk.X)
        
        tk.Button(btn_frame, text="Browse Folder", command=self.browse, 
                  bg=self.accent_color, fg="white", font=("Helvetica", 11, "bold"), 
                  relief="flat", height=2, activebackground="#a78bfa").pack(
                  side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        tk.Button(btn_frame, text="Load Repo", command=self.load_repository, 
                  bg=self.success_color, fg="white", font=("Helvetica", 11, "bold"), 
                  relief="flat", height=2, activebackground="#4ade80").pack(
                  side=tk.LEFT, fill=tk.X, expand=True)
        
        # Project Name section
        tk.Label(left, text="Project Name", font=("Helvetica", 14, "bold"), 
                 bg=self.panel_color, fg=self.fg_color).pack(anchor="w", padx=25, pady=(20, 8))
        
        project_entry = tk.Entry(left, textvariable=self.project_name_var, font=("Consolas", 12), 
                        bg="#1f1f2e", fg=self.fg_color, relief="flat", bd=0, 
                        highlightthickness=2, highlightbackground=self.accent_color, 
                        highlightcolor=self.accent_color, insertbackground=self.fg_color)
        project_entry.pack(fill=tk.X, padx=25, pady=8, ipady=8)
        
        # RIGHT: Status + interactive Project Structure panels
        right = tk.Frame(main_frame, bg=self.panel_color)
        right.grid(row=0, column=1, sticky="nsew")
        
        # Repository Status
        header_frame = tk.Frame(right, bg=self.panel_color)
        header_frame.pack(fill=tk.X, padx=20, pady=(15, 8))
        
        tk.Label(header_frame, text="Repository Status", font=("Helvetica", 16, "bold"), 
                 bg=self.panel_color, fg=self.fg_color).pack(side=tk.LEFT)
        
        tk.Button(header_frame, text="Refresh", command=self.load_repository, 
                  bg=self.panel_color, fg=self.accent_color, font=("Helvetica", 10, "bold"), 
                  relief="flat", activebackground="#1f1f2e").pack(side=tk.RIGHT)
        
        self.status_text = tk.Text(right, bg="#1a1a2b", fg="#a5b4fc", font=("Consolas", 12),
                                  relief="flat", padx=18, pady=18, wrap=tk.WORD, state="disabled")
        self.status_text.pack(fill=tk.BOTH, expand=False, padx=15, pady=(0, 8), ipady=120)
        
        status_scrollbar = ttk.Scrollbar(right, command=self.status_text.yview)
        status_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 8))
        self.status_text.config(yscrollcommand=status_scrollbar.set)
        
        # Configure colored tags for status
        self.status_text.tag_config("success", foreground=self.success_color)
        self.status_text.tag_config("warning", foreground=self.warning_color)
        self.status_text.tag_config("error", foreground=self.error_color)
        self.status_text.tag_config("info", foreground=self.fg_color)
        
        # Interactive two-column Project Structure (scrollable rows + dynamic buttons)
        structure_header = tk.Frame(right, bg=self.panel_color)
        structure_header.pack(fill=tk.X, padx=20, pady=(12, 8))
        
        tk.Label(structure_header, text="Project Structure", font=("Helvetica", 16, "bold"), 
                 bg=self.panel_color, fg=self.fg_color).pack(side=tk.LEFT)
        
        self.structure_canvas = tk.Canvas(right, bg="#1a1a2b", highlightthickness=0)
        self.structure_canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        structure_scrollbar = ttk.Scrollbar(right, orient="vertical", command=self.structure_canvas.yview)
        structure_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 15))
        self.structure_canvas.configure(yscrollcommand=structure_scrollbar.set)
        
        self.structure_inner = tk.Frame(self.structure_canvas, bg="#1a1a2b")
        self.structure_canvas.create_window((0, 0), window=self.structure_inner, anchor="nw")
        
        self.structure_inner.bind("<Configure>", 
                                  lambda e: self.structure_canvas.configure(scrollregion=self.structure_canvas.bbox("all")))
        
        # Make columns expandable
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
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
            return
        
        # Use the dedicated helper (no duplication!)
        status_data = get_repo_status(path, self.project_name_var.get().strip())
        
        # Sync project name back to UI (handles auto-fill from basename)
        self.project_name_var.set(status_data["project_name"])
        
        # Render all status lines with their proper color tags
        for text, tag in status_data.get("status_lines", []):
            self.status_text.insert(tk.END, text, tag)
        
        self.status_text.config(state="disabled")
        
        # Populate the interactive two-column Project Structure
        self._populate_structure(path)
        
    def _get_file_status_map(self, root_path: str) -> dict:
        """Return dict of relative path -> color tag for background coloring."""
        status_map = {}
        if not os.path.exists(os.path.join(root_path, ".git")):
            return status_map
        try:
            output = subprocess.check_output(
                ["git", "-C", root_path, "status", "--porcelain", "-uall"],
                text=True, stderr=subprocess.STDOUT
            ).strip()
            for line in output.splitlines():
                if not line:
                    continue
                code = line[:2].strip()
                rel_path = line[3:].strip()
                if code.startswith("?"):
                    status_map[rel_path] = "untracked"
                else:
                    status_map[rel_path] = "modified"
        except Exception:
            pass  # graceful fallback
        return status_map
        
    def _is_ignored(self, rel_path: str, root_path: str) -> bool:
        """Check if the relative path appears in .gitignore (exact line match)."""
        gitignore_path = os.path.join(root_path, ".gitignore")
        if not os.path.exists(gitignore_path):
            return False
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f.readlines() if line.strip() and not line.startswith("#")]
            return rel_path in lines
        except Exception:
            return False
        
    def _populate_structure(self, root_path: str):
        """Build two-column rows (name + dynamic ❌ / ♻️ button) with greyed-out styling for ignored items."""
        # Clear any previous rows
        for widget in self.structure_inner.winfo_children():
            widget.destroy()
        
        status_map = self._get_file_status_map(root_path)
        row = 0
        
        try:
            for dirpath, dirnames, filenames in os.walk(root_path):
                # Skip .git directory entirely
                if ".git" in dirnames:
                    dirnames.remove(".git")
                
                level = dirpath.replace(root_path, "").count(os.sep)
                indent = "│   " * level
                
                # Directory row
                rel_dir = os.path.relpath(dirpath, root_path)
                if rel_dir == ".":
                    rel_dir = "."
                is_ignored_dir = self._is_ignored(rel_dir, root_path)
                dir_fg = self.grey_color if is_ignored_dir else "#a5b4fc"
                dir_frame = tk.Frame(self.structure_inner, bg="#1a1a2b")
                dir_frame.grid(row=row, column=0, sticky="ew", padx=10, pady=4)
                tk.Label(dir_frame, text=f"{indent}📁 {rel_dir}/", 
                         bg="#1a1a2b", fg=dir_fg, font=("Consolas", 11)).pack(side=tk.LEFT)
                # Dynamic button for directories too
                btn_text = "♻️" if is_ignored_dir else "❌"
                btn_cmd = lambda p=rel_dir, r=root_path: self.remove_from_gitignore(p, r) if is_ignored_dir else self.add_to_gitignore(p, r)
                tk.Button(dir_frame, text=btn_text, fg="#ef4444" if not is_ignored_dir else "#eab308", 
                          bg="#1a1a2b", font=("Helvetica", 14, "bold"), relief="flat", width=3,
                          command=btn_cmd).pack(side=tk.RIGHT, padx=10)
                row += 1
                
                # File rows
                file_indent = "│   " * (level + 1)
                for f in sorted(filenames):
                    rel_file = os.path.join(rel_dir, f) if rel_dir != "." else f
                    tag = status_map.get(rel_file, "clean")
                    is_ignored = self._is_ignored(rel_file, root_path)
                    fg_color = self.grey_color if is_ignored else ("#f87171" if tag == "untracked" else "#facc15" if tag == "modified" else "#a5b4fc")
                    
                    file_frame = tk.Frame(self.structure_inner, bg="#1a1a2b")
                    file_frame.grid(row=row, column=0, sticky="ew", padx=10, pady=2)
                    
                    # Column 1: indented file name (greyed if ignored)
                    tk.Label(file_frame, text=f"{file_indent}📄 {f}", 
                             bg="#1a1a2b", fg=fg_color, font=("Consolas", 11)).pack(side=tk.LEFT)
                    
                    # Column 2: dynamic button (❌ or ♻️)
                    btn_text = "♻️" if is_ignored else "❌"
                    btn_cmd = lambda p=rel_file, r=root_path: self.remove_from_gitignore(p, r) if is_ignored else self.add_to_gitignore(p, r)
                    tk.Button(file_frame, text=btn_text, fg="#ef4444" if not is_ignored else "#eab308", 
                              bg="#1a1a2b", font=("Helvetica", 14, "bold"), relief="flat", width=3,
                              command=btn_cmd).pack(side=tk.RIGHT, padx=10)
                    row += 1
                    
                # Prevent huge trees from freezing UI
                if level > 6:
                    tk.Label(self.structure_inner, text="   ... (deeper levels truncated for performance)", 
                             bg="#1a1a2b", fg="#a5b4fc", font=("Consolas", 11)).grid(row=row, column=0, sticky="w", padx=10)
                    break
                    
        except Exception as e:
            tk.Label(self.structure_inner, text=f"❌ Could not read structure: {e}", 
                     bg="#1a1a2b", fg="#ef4444").grid(row=row, column=0, sticky="w", padx=10)
        
    def add_to_gitignore(self, rel_path: str, root_path: str):
        """Append the selected item to .gitignore and refresh the entire view."""
        gitignore_path = os.path.join(root_path, ".gitignore")
        try:
            with open(gitignore_path, "a", encoding="utf-8") as f:
                f.write(f"\n{rel_path}\n")
            self.load_repository()  # refresh instantly
        except Exception as e:
            print(f"Failed to update .gitignore: {e}")
        
    def remove_from_gitignore(self, rel_path: str, root_path: str):
        """Remove the selected item from .gitignore (exact line match) and refresh."""
        gitignore_path = os.path.join(root_path, ".gitignore")
        if not os.path.exists(gitignore_path):
            return
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            with open(gitignore_path, "w", encoding="utf-8") as f:
                for line in lines:
                    if line.strip() != rel_path:
                        f.write(line)
            self.load_repository()  # refresh instantly
        except Exception as e:
            print(f"Failed to update .gitignore: {e}")

if __name__ == "__main__":
    app = GitSquisherGUI()
    app.root.mainloop()
