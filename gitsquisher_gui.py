import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import os
from repo_status import get_repo_status
from git_structure import build_interactive_structure
from gitignore_manager import add_to_gitignore, remove_from_gitignore
from squisher import create_squish, list_squishable_files
from squisher_encrypt import encrypt_squish
from ignore_template import apply_ignore_template
from squisher_shutdown import safe_shutdown

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
        
        # LIVE PREVIEW COUNTER
        self.preview_label = tk.Label(left, text="📦 0 clean files will be squished", 
                                     font=("Helvetica", 12, "bold"), bg=self.panel_color, 
                                     fg="#fb923c", anchor="w")
        self.preview_label.pack(anchor="w", padx=25, pady=(15, 5))
        
        # SQUISH BUTTON with grapes emoji
        squish_btn = tk.Button(left, text="🗜️ Squish (Zip) 🍇", command=self.squish_project,
                               bg="#22c55e", fg="white", font=("Helvetica", 14, "bold"),
                               relief="flat", height=3, activebackground="#4ade80")
        squish_btn.pack(pady=15, padx=25, fill=tk.X)
        
        # ENCRYPT & KEY BUTTON
        encrypt_btn = tk.Button(left, text="🔐 Encrypt & Key", command=self.encrypt_project,
                               bg="#8b5cf6", fg="white", font=("Helvetica", 14, "bold"),
                               relief="flat", height=3, activebackground="#a78bfa")
        encrypt_btn.pack(pady=8, padx=25, fill=tk.X)
        
        # APPLY ADVANCED .GITIGNORE BUTTON (completes the main debloat protocol)
        template_btn = tk.Button(left, text="📋 Apply Advanced .gitignore", command=self.apply_template,
                                 bg="#eab308", fg="white", font=("Helvetica", 11, "bold"),
                                 relief="flat", height=2, activebackground="#fcd34d")
        template_btn.pack(pady=8, padx=25, fill=tk.X)
        
        # EXIT BUTTON
        exit_btn = tk.Button(left, text="✕ Exit GitSquisher", command=self.exit_app,
                             bg="#ef4444", fg="white", font=("Helvetica", 11, "bold"),
                             relief="flat", height=2, activebackground="#f87171")
        exit_btn.pack(pady=12, padx=25, fill=tk.X)
        
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
        
        # Interactive two-column Project Structure
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
        try:
            dir_path = filedialog.askdirectory(title="Select Project Root Directory")
            if dir_path:
                self.path_var.set(dir_path)
                self.load_repository()
        except Exception as e:
            messagebox.showwarning("Graceful Warning", f"Browse failed (non-critical): {e}")
            
    def load_repository(self):
        try:
            path = self.path_var.get().strip()
            self.status_text.config(state="normal")
            self.status_text.delete(1.0, tk.END)
            
            if not path:
                self.status_text.insert(tk.END, "❌ Please select or enter a directory path.\n", "error")
                self.status_text.config(state="disabled")
                self.preview_label.config(text="📦 0 clean files will be squished")
                return
            
            # AUTO-APPLY advanced .gitignore template (completes main debloat protocol)
            success, msg = apply_ignore_template(path, self.project_name_var.get().strip())
            if success:
                self.status_text.insert(tk.END, f"{msg}\n", "success")
            else:
                self.status_text.insert(tk.END, f"{msg}\n", "warning")
            
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
        except Exception as e:
            self.status_text.config(state="normal")
            self.status_text.insert(tk.END, f"⚠️ Graceful load error (non-fatal): {e}\n", "warning")
            self.status_text.config(state="disabled")
            messagebox.showwarning("Graceful Warning", f"Load encountered an issue but app continues: {e}")
        
    def apply_template(self):
        """One-click apply of the advanced .gitignore template."""
        path = self.path_var.get().strip()
        if not path:
            messagebox.showerror("Error", "Please load a project directory first.")
            return
        project_name = self.project_name_var.get().strip() or os.path.basename(path)
        success, msg = apply_ignore_template(path, project_name)
        if success:
            messagebox.showinfo("Success", msg)
            self.load_repository()  # refresh everything
        else:
            messagebox.showerror("Template Error", msg)
        
    def _populate_structure(self, root_path: str):
        try:
            for widget in self.structure_inner.winfo_children():
                widget.destroy()
            
            rows = build_interactive_structure(root_path)
            for idx, row_data in enumerate(rows):
                frame = tk.Frame(self.structure_inner, bg="#1a1a2b")
                frame.grid(row=idx, column=0, sticky="ew", padx=10, pady=4 if row_data["type"] == "dir" else 2)
                
                tk.Label(frame, text=f"{row_data['indent']}{row_data['display_name']}", 
                         bg="#1a1a2b", fg=row_data["fg_color"], font=("Consolas", 11)).pack(side=tk.LEFT)
                
                if row_data["button_text"]:
                    btn_text = row_data["button_text"]
                    btn_fg = row_data["button_fg"]
                    rel_path = row_data["rel_path"]
                    is_ignored = row_data["is_ignored"]
                    btn_cmd = lambda p=rel_path, r=root_path, ign=is_ignored: self._remove_from_gitignore(p, r) if ign else self._add_to_gitignore(p, r)
                    tk.Button(frame, text=btn_text, fg=btn_fg, 
                              bg="#1a1a2b", font=("Helvetica", 14, "bold"), relief="flat", width=3,
                              command=btn_cmd).pack(side=tk.RIGHT, padx=10)
        except Exception as e:
            tk.Label(self.structure_inner, text=f"❌ Could not read structure (graceful fallback): {e}", 
                     bg="#1a1a2b", fg="#ef4444").grid(row=0, column=0, sticky="w", padx=10)
        
    def _add_to_gitignore(self, rel_path: str, root_path: str):
        add_to_gitignore(rel_path, root_path)
        self.load_repository()
        
    def _remove_from_gitignore(self, rel_path: str, root_path: str):
        remove_from_gitignore(rel_path, root_path)
        self.load_repository()
        
    def squish_project(self):
        try:
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
        except Exception as e:
            self.status_text.insert(tk.END, f"⚠️ Squish encountered non-fatal error: {e}\n", "warning")
            messagebox.showwarning("Graceful Warning", f"Squish failed gracefully: {e}")
        finally:
            self.status_text.config(state="disabled")
            self.load_repository()
        
    def encrypt_project(self):
        try:
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
        except Exception as e:
            self.status_text.insert(tk.END, f"⚠️ Encrypt encountered non-fatal error: {e}\n", "warning")
            messagebox.showwarning("Graceful Warning", f"Encrypt failed gracefully: {e}")
        finally:
            self.status_text.config(state="disabled")
            self.load_repository()
        
    def exit_app(self):
        """Graceful exit using the dedicated safe shutdown helper."""
        safe_shutdown(self.root)

if __name__ == "__main__":
    try:
        app = GitSquisherGUI()
        app.root.mainloop()
    except Exception as e:
        # Final safety net at entry point
        print(f"GitSquisher encountered a fatal startup issue (graceful exit): {e}")
        safe_shutdown()
