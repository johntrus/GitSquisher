import tkinter as tk
from tkinter import ttk

def show_help_window(root: tk.Tk) -> None:
    """Open a clean, modern modal Help window with a complete glossary of every button in GitSquisher.

    This is the single source of truth for user-facing help text.
    Called from the new Help button in the main GUI.
    """
    help_win = tk.Toplevel(root)
    help_win.title("GitSquisher Help – Button Glossary")
    help_win.geometry("720x620")
    help_win.configure(bg="#141425")
    help_win.transient(root)
    help_win.grab_set()
    help_win.resizable(True, True)

    # Header
    tk.Label(help_win, text="🗜️ GitSquisher Help", font=("Helvetica", 20, "bold"),
             bg="#141425", fg="#c3c8ff").pack(pady=15)

    tk.Label(help_win, text="Click any button in the main window to see what it does.",
             font=("Helvetica", 11), bg="#141425", fg="#9ca3af").pack(pady=(0, 15))

    # Scrollable glossary
    main_frame = tk.Frame(help_win, bg="#141425")
    main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=10)

    canvas = tk.Canvas(main_frame, bg="#1a1a2b", highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#1a1a2b")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Glossary entries (button label → description)
    glossary = [
        ("Browse Folder", "Opens a folder picker so you can select any project directory to work with."),
        ("Load Repo", "Scans the selected folder, shows Git status, live file count, and builds the interactive project tree."),
        ("🗜️ Squish (Zip) 🍇", "Creates a clean, .gitignore-respecting zip archive of your entire project and saves it in the squishes/ folder."),
        ("🔐 Encrypt & Key", "Automatically creates a fresh squish, encrypts it with AES-256 (Fernet), and handles automatic key rotation every 90 days."),
        ("🔓 Decrypt Latest", "Decrypts the most recent .enc file back into a usable _decrypted.zip using the current or any previous key."),
        ("Refresh", "Reloads the repository status and project structure without leaving the app."),
        ("❓ Help", "Opens this exact help window so you can quickly understand every button."),
        ("✕ Exit GitSquisher", "Performs a graceful, verified shutdown with animated progress and safely closes the application."),
    ]

    for label, desc in glossary:
        row = tk.Frame(scrollable_frame, bg="#1a1a2b")
        row.pack(fill=tk.X, pady=6, padx=10)

        # Button label pill
        tk.Label(row, text=label, font=("Consolas", 11, "bold"),
                 bg="#8b5cf6", fg="white", padx=10, pady=4).pack(side=tk.LEFT)

        # Description
        tk.Label(row, text=desc, font=("Helvetica", 11),
                 bg="#1a1a2b", fg="#c3c8ff", anchor="w", justify="left", wraplength=480).pack(
                 side=tk.LEFT, padx=12, pady=2)

    # === USAGE GUIDE (3 honest paragraphs as requested) ===
    tk.Label(scrollable_frame, text="\nHow to Use GitSquisher", font=("Helvetica", 14, "bold"),
             bg="#1a1a2b", fg="#22c55e").pack(anchor="w", padx=10, pady=(20, 5))

    para1 = ("GitSquisher is intentionally simple and safe. First click “Browse Folder” or type a path, then “Load Repo”. "
             "You will instantly see your project status, live file count, and an interactive tree where you can toggle "
             "files into/out of .gitignore. Once loaded you can freely Squish, Encrypt, or Decrypt. Expect the Squish button "
             "to create a clean zip in under a second for most projects; larger repos may take a few seconds but will always "
             "respect your .gitignore and never include the squishes/ folder itself.")

    para2 = ("The “🔐 Encrypt & Key” button does exactly what it says: it first creates a fresh squish, then automatically "
             "encrypts it with AES-256. If your encryption key is older than 90 days it will transparently rotate the key "
             "and re-encrypt every existing .enc file for you. You will see a clear success message with the new .enc filename. "
             "The key file (grem_encryption.key) is automatically ignored and never committed to git.")

    para3 = ("The “🔓 Decrypt Latest” button instantly turns the newest .enc file back into a normal zip you can unzip anywhere. "
             "Because of MultiFernet rotation support, it will still work even if you have rotated the key multiple times. "
             "All operations are non-destructive — your original files are untouched. If anything ever fails you will see a "
             "clear red error in the status panel. The app is designed so you can safely experiment without risk to your project.")

    for p in (para1, para2, para3):
        tk.Label(scrollable_frame, text=p, font=("Helvetica", 11),
                 bg="#1a1a2b", fg="#c3c8ff", anchor="w", justify="left", wraplength=620).pack(
                 anchor="w", padx=10, pady=8)

    # Close button at bottom
    close_btn = tk.Button(help_win, text="Close Help", command=help_win.destroy,
                          bg="#ef4444", fg="white", font=("Helvetica", 12, "bold"),
                          relief="flat", height=2, activebackground="#f87171")
    close_btn.pack(pady=20)

    # Keyboard shortcut hint
    tk.Label(help_win, text="Tip: Press Escape to close this window", font=("Helvetica", 9),
             bg="#141425", fg="#9ca3af").pack(pady=(0, 15))
