import tkinter as tk
from tkinter import ttk

def create_widgets(gui: 'GitSquisherGUI') -> None:
    """Create and layout all widgets for the GitSquisher GUI.

    This extracted function keeps gitsquisher_gui.py lean and focused solely on behavior.
    All Tkinter objects are attached back to the gui instance so the rest of the class
    can reference them (status_text, structure_inner, preview_label, etc.).
    Maintains the exact modern dark-night look, responsive layout, and emoji-rich UX.
    """
    # Main container with two columns using grid for better responsiveness
    main_frame = tk.Frame(gui.root, bg=gui.style.bg_color)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # LEFT: Controls panel
    left = tk.Frame(main_frame, bg=gui.style.panel_color, width=420)
    left.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
    left.grid_propagate(False)

    tk.Label(left, text="GitSquisher", font=gui.style.title_font,
             bg=gui.style.panel_color, fg=gui.style.accent_color).pack(pady=25)

    tk.Label(left, text="Project Directory", font=gui.style.label_font,
             bg=gui.style.panel_color, fg=gui.style.fg_color).pack(anchor="w", padx=25, pady=(0, 8))

    entry = tk.Entry(left, textvariable=gui.path_var, font=gui.style.mono_font,
                     bg="#1f1f2e", fg=gui.style.fg_color, relief="flat", bd=0,
                     highlightthickness=2, highlightbackground=gui.style.accent_color,
                     highlightcolor=gui.style.accent_color, insertbackground=gui.style.fg_color)
    entry.pack(fill=tk.X, padx=25, pady=8, ipady=8)

    btn_frame = tk.Frame(left, bg=gui.style.panel_color)
    btn_frame.pack(pady=12, padx=25, fill=tk.X)

    tk.Button(btn_frame, text="Browse Folder", command=gui.browse,
              bg=gui.style.accent_color, fg="white", font=gui.style.small_button_font,
              relief="flat", height=2, activebackground="#a78bfa").pack(
              side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

    tk.Button(btn_frame, text="Load Repo", command=gui.load_repository,
              bg=gui.style.success_color, fg="white", font=gui.style.small_button_font,
              relief="flat", height=2, activebackground="#4ade80").pack(
              side=tk.LEFT, fill=tk.X, expand=True)

    # Project Name section
    tk.Label(left, text="Project Name", font=gui.style.label_font,
             bg=gui.style.panel_color, fg=gui.style.fg_color).pack(anchor="w", padx=25, pady=(20, 8))

    project_entry = tk.Entry(left, textvariable=gui.project_name_var, font=gui.style.mono_font,
                             bg="#1f1f2e", fg=gui.style.fg_color, relief="flat", bd=0,
                             highlightthickness=2, highlightbackground=gui.style.accent_color,
                             highlightcolor=gui.style.accent_color, insertbackground=gui.style.fg_color)
    project_entry.pack(fill=tk.X, padx=25, pady=8, ipady=8)

    # LIVE PREVIEW COUNTER
    gui.preview_label = tk.Label(left, text="📦 0 clean files will be squished",
                                 font=("Helvetica", 12, "bold"), bg=gui.style.panel_color,
                                 fg="#fb923c", anchor="w")
    gui.preview_label.pack(anchor="w", padx=25, pady=(15, 5))

    # SQUISH BUTTON
    squish_btn = tk.Button(left, text="🗜️ Squish (Zip) 🍇", command=gui.squish_project,
                           bg="#22c55e", fg="white", font=gui.style.button_font,
                           relief="flat", height=3, activebackground="#4ade80")
    squish_btn.pack(pady=15, padx=25, fill=tk.X)

    # ENCRYPT & KEY BUTTON
    encrypt_btn = tk.Button(left, text="🔐 Encrypt & Key", command=gui.encrypt_project,
                            bg="#8b5cf6", fg="white", font=gui.style.button_font,
                            relief="flat", height=3, activebackground="#a78bfa")
    encrypt_btn.pack(pady=8, padx=25, fill=tk.X)

    # DECRYPT LATEST BUTTON
    decrypt_btn = tk.Button(left, text="🔓 Decrypt Latest", command=gui.decrypt_project,
                            bg="#06b67f", fg="white", font=gui.style.button_font,
                            relief="flat", height=3, activebackground="#34d399")
    decrypt_btn.pack(pady=8, padx=25, fill=tk.X)

    # HELP BUTTON (new, harmoniously placed before Exit)
    help_btn = tk.Button(left, text="❓ Help", command=gui.show_help,
                         bg="#eab308", fg="white", font=gui.style.small_button_font,
                         relief="flat", height=2, activebackground="#fcd34d")
    help_btn.pack(pady=12, padx=25, fill=tk.X)

    # EXIT BUTTON
    exit_btn = tk.Button(left, text="✕ Exit GitSquisher", command=gui.exit_app,
                         bg="#ef4444", fg="white", font=gui.style.small_button_font,
                         relief="flat", height=2, activebackground="#f87171")
    exit_btn.pack(pady=8, padx=25, fill=tk.X)

    # RIGHT: Status + interactive Project Structure panels
    right = tk.Frame(main_frame, bg=gui.style.panel_color)
    right.grid(row=0, column=1, sticky="nsew")

    right.rowconfigure(0, weight=35)
    right.rowconfigure(1, weight=65)

    # Repository Status
    header_frame = tk.Frame(right, bg=gui.style.panel_color)
    header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 4))

    tk.Label(header_frame, text="Repository Status", font=gui.style.header_font,
             bg=gui.style.panel_color, fg=gui.style.fg_color).pack(side=tk.LEFT)

    tk.Button(header_frame, text="Refresh", command=gui.load_repository,
              bg=gui.style.panel_color, fg=gui.style.accent_color, font=("Helvetica", 10, "bold"),
              relief="flat", activebackground="#1f1f2e").pack(side=tk.RIGHT)

    gui.status_text = tk.Text(right, bg="#1a1a2b", fg="#a5b4fc", font=gui.style.status_font,
                              relief="flat", padx=18, pady=12, wrap=tk.WORD, state="disabled", height=8)
    gui.status_text.grid(row=0, column=0, sticky="nsew", padx=15, pady=(0, 8))

    status_scrollbar = ttk.Scrollbar(right, command=gui.status_text.yview)
    status_scrollbar.grid(row=0, column=1, sticky="ns", pady=(0, 8))
    gui.status_text.config(yscrollcommand=status_scrollbar.set)

    gui.status_text.tag_config("success", foreground=gui.style.success_color)
    gui.status_text.tag_config("warning", foreground=gui.style.warning_color)
    gui.status_text.tag_config("error", foreground=gui.style.error_color)
    gui.status_text.tag_config("info", foreground=gui.style.fg_color)

    # Project Structure
    structure_header = tk.Frame(right, bg=gui.style.panel_color)
    structure_header.grid(row=1, column=0, sticky="ew", padx=20, pady=(8, 8))

    tk.Label(structure_header, text="Project Structure", font=gui.style.header_font,
             bg=gui.style.panel_color, fg=gui.style.fg_color).pack(side=tk.LEFT)

    gui.structure_canvas = tk.Canvas(right, bg="#1a1a2b", highlightthickness=0)
    gui.structure_canvas.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))

    structure_scrollbar = ttk.Scrollbar(right, orient="vertical", command=gui.structure_canvas.yview)
    structure_scrollbar.grid(row=1, column=1, sticky="ns", pady=(0, 15))
    gui.structure_canvas.configure(yscrollcommand=structure_scrollbar.set)

    gui.structure_inner = tk.Frame(gui.structure_canvas, bg="#1a1a2b")
    gui.structure_canvas.create_window((0, 0), window=gui.structure_inner, anchor="nw")

    gui.structure_inner.bind("<Configure>",
                             lambda e: gui.structure_canvas.configure(scrollregion=gui.structure_canvas.bbox("all")))

    # Make columns expandable
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(0, weight=1)
