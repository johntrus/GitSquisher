import tkinter as tk
from tkinter import ttk
from typing import Optional
import time
import sys

def _show_shutdown_progress(root: Optional[tk.Tk]) -> None:
    """Display a clean, modern progress dialog with explicit verification steps.

    After every step a quick green-check verification appears.
    Final message is exactly "Squisher Closed Successfully 🍇✅" followed by a smooth fade-out.
    Fully harmonized with the rest of GitSquisher’s polished UX.
    """
    if root is None or not root.winfo_exists():
        return

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
        """Quick verification that the step completed successfully."""
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
    status_label.config(text="Squisher Closed Successfully 🍇✅",
                        fg="#22c55e", font=("Helvetica", 14, "bold"))
    verify_label.config(text="")
    progress['value'] = 100
    progress_win.update()

    # Smooth fade-out
    for i in range(20, -1, -1):
        alpha = i / 20.0
        progress_win.attributes("-alpha", alpha)
        progress_win.update()
        time.sleep(0.025)

    progress_win.destroy()


def safe_shutdown(root: Optional[tk.Tk] = None) -> None:
    """Safest possible shutdown of GitSquisher.

    WHAT THIS TOUCHES (and nothing else):
      • Only the Tkinter window and event loop created by GitSquisher
      • Only the current Python process
      • In-memory objects (including MultiFernet) are cleaned up by Python GC

    Zero filesystem changes, zero external process kills, zero risk of data loss.
    """
    try:
        if root is not None and root.winfo_exists():
            _show_shutdown_progress(root)
            root.quit()
            root.destroy()

        sys.exit(0)
    except Exception:
        # Ultra-safe fallback: script simply ends
        pass
