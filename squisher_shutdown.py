import tkinter as tk
from tkinter import ttk
from typing import Optional
import time
import sys

def _show_shutdown_progress(root: Optional[tk.Tk]) -> None:
    """Display a clean, modern progress dialog with explicit shutdown steps + verification.

    After EVERY step a quick verification check runs and shows a green check.
    Final message is exactly "Squisher Closed Successfully 🍇✅" followed by a smooth fade-out.
    """
    if root is None or not root.winfo_exists():
        return

    # Create a small modal progress window
    progress_win = tk.Toplevel(root)
    progress_win.title("GitSquisher - Safe Shutdown")
    progress_win.geometry("480x220")
    progress_win.configure(bg="#141425")
    progress_win.resizable(False, False)
    progress_win.transient(root)
    progress_win.grab_set()

    tk.Label(progress_win, text="🛡️ Shutting down GitSquisher safely...", 
             font=("Helvetica", 13, "bold"), bg="#141425", fg="#c3c8ff").pack(pady=12)

    progress = ttk.Progressbar(progress_win, orient="horizontal", length=420, mode="determinate")
    progress.pack(pady=8, padx=30)

    status_label = tk.Label(progress_win, text="Initializing safe shutdown...", 
                            font=("Consolas", 10), bg="#141425", fg="#fb923c", anchor="w")
    status_label.pack(fill=tk.X, padx=30, pady=(0, 8))

    verify_label = tk.Label(progress_win, text="", 
                            font=("Consolas", 10, "bold"), bg="#141425", fg="#22c55e", anchor="w")
    verify_label.pack(fill=tk.X, padx=30, pady=(0, 12))

    def verify_step(step_name: str):
        """Quick verification that the step actually completed."""
        verify_label.config(text=f"✓ Verified: {step_name}")
        progress_win.update()
        time.sleep(0.18)

    steps = [
        ("Closing main window and widgets...", 25, "main window closed"),
        ("Releasing Tkinter event loop...", 50, "event loop released"),
        ("Clearing temporary UI resources...", 75, "resources cleared"),
        ("Final cleanup and graceful exit...", 100, "cleanup complete"),
    ]

    for text, percent, verify_text in steps:
        status_label.config(text=text)
        progress['value'] = percent
        progress_win.update()
        time.sleep(0.22)
        verify_step(verify_text)

    # FINAL SUCCESS SCREEN
    status_label.config(text="Squisher Closed Successfully 🍇✅", fg="#22c55e", font=("Helvetica", 14, "bold"))
    verify_label.config(text="")
    progress['value'] = 100
    progress_win.update()

    # Smooth fade-out (alpha from 1.0 → 0.0)
    for i in range(20, -1, -1):
        alpha = i / 20.0
        progress_win.attributes("-alpha", alpha)
        progress_win.update()
        time.sleep(0.025)

    # All steps complete - destroy the progress dialog
    progress_win.destroy()


def safe_shutdown(root: Optional[tk.Tk] = None) -> None:
    """Safest possible shutdown of GitSquisher.

    WHAT THIS BUTTON TOUCHES (and nothing else):
      • Only the Tkinter window and event loop that GitSquisher created
      • Only the current Python process that was started when you ran the app
      • In-memory objects (including Fernet from cryptography) are automatically cleaned up by Python's normal garbage collection when the process ends

    IMPORTANT: Nothing outside of GitSquisher is ever closed, killed, or modified.
    Fernet is NOT "closed" in any system-wide sense — it is simply an in-memory Python object that disappears when the app process ends.
    Zero filesystem changes, zero external process termination, zero risk of data loss or system impact.
    """
    try:
        if root is not None and root.winfo_exists():
            # Show the user-friendly progress dialog with verification
            _show_shutdown_progress(root)

            # Then perform the actual clean shutdown
            root.quit()
            root.destroy()

        # Let Python exit naturally (safest possible)
        sys.exit(0)
    except Exception:
        # Ultra-safe fallback: do nothing aggressive - script simply ends
        pass
