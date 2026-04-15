class SquisherStyle:
    """Centralized night-mode color palette, fonts, and visual constants for GitSquisher.

    All colors, fonts, and accents are defined once here so every GUI file stays clean,
    consistent, and easy to evolve. Updated for full harmony with the new Decrypt button
    and polished modern UX while preserving the original deep-contrast aesthetic.
    """
    def __init__(self):
        # Night time color scheme (refined for deeper contrast and modern feel)
        self.bg_color = "#0a0a14"
        self.panel_color = "#141425"
        self.fg_color = "#c3c8ff"
        self.accent_color = "#8b5cf6"
        self.success_color = "#22c55e"
        self.warning_color = "#eab308"
        self.error_color = "#ef4444"
        self.grey_color = "#9ca3af"          # for ignored items
        self.decrypt_color = "#06b67f"       # new harmonious teal for Decrypt button

        # Font definitions (kept consistent across the entire GUI)
        self.title_font = ("Helvetica", 28, "bold")
        self.header_font = ("Helvetica", 16, "bold")
        self.label_font = ("Helvetica", 14, "bold")
        self.button_font = ("Helvetica", 14, "bold")
        self.small_button_font = ("Helvetica", 11, "bold")
        self.mono_font = ("Consolas", 12)
        self.status_font = ("Consolas", 12)
        self.structure_font = ("Consolas", 11)
