import tkinter as tk
from .themes import THEMES

class AeroApp(tk.Tk):
    def __init__(self, title="AeroTk App", size=(800, 500), theme="dark"):
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.minsize(400, 300)
        
        self.current_theme = theme if theme in THEMES else "dark"
        self.colors = THEMES[self.current_theme]
        self._widgets = []
        
        self.configure(bg=self.colors["bg"])

    def register_widget(self, widget):
        self._widgets.append(widget)

    def set_theme(self, theme_name):
        if theme_name in THEMES:
            self.current_theme = theme_name
            self.colors = THEMES[theme_name]
            self.configure(bg=self.colors["bg"])
            for w in self._widgets:
                if hasattr(w, "update_theme"):
                    w.update_theme()

    def run(self):
        self.mainloop()
