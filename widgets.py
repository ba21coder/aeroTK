# aerotk/widgets.py

import tkinter as tk

class _AeroBase(tk.Canvas):
    def __init__(self, master, width, height, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, bd=0, **kwargs)
        self.w = width
        self.h = height
        
        self.app = master
        while not hasattr(self.app, "colors") and getattr(self.app, "master", None):
            self.app = self.app.master
            
        if hasattr(self.app, "register_widget"):
            self.app.register_widget(self)

    @property
    def colors(self):
        return getattr(self.app, "colors", {
            "bg": "#0f172a", "fg": "#f8fafc", "fg_muted": "#94a3b8",
            "card": "#1e293b", "border": "#334155", "accent": "#3b82f6",
            "accent_hover": "#2563eb", "input_bg": "#020617", "switch_off": "#475569"
        })

    def _get_parent_bg(self):
        if hasattr(self.master, "bg_color"):
            return self.master.bg_color
        try:
            return self.master.cget("bg")
        except Exception:
            return self.colors["bg"]

    def _round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1+r, y1, x2-r, y1, x2, y1, x2, y1+r,
            x2, y2-r, x2, y2, x2-r, y2, x1+r, y2,
            x1, y2, x1, y2-r, x1, y1+r, x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)


class AeroFrame(_AeroBase):
    def __init__(self, master, width=300, height=200, radius=14, **kwargs):
        super().__init__(master, width, height, **kwargs)
        self.radius = radius
        self.bg_color = self.colors["card"]
        self.draw()

    def draw(self):
        self.delete("all")
        self.bg_color = self.colors["card"]
        self.configure(bg=self._get_parent_bg())
        self._round_rect(1, 1, self.w-1, self.h-1, self.radius, fill=self.bg_color, outline=self.colors["border"])

    def update_theme(self):
        self.draw()
        for child in self.winfo_children():
            if hasattr(child, "update_theme"):
                child.update_theme()


class AeroLabel(tk.Label):
    def __init__(self, master, text="", size=11, weight="normal", muted=False, **kwargs):
        self.muted = muted
        self.app = master
        while not hasattr(self.app, "colors") and getattr(self.app, "master", None):
            self.app = self.app.master
        if hasattr(self.app, "register_widget"):
            self.app.register_widget(self)
            
        super().__init__(master, text=text, font=("Segoe UI", size, weight), **kwargs)
        self.update_theme()

    def update_theme(self):
        colors = self.app.colors
        bg = getattr(self.master, "bg_color", colors["bg"])
        fg = colors["fg_muted"] if self.muted else colors["fg"]
        self.configure(bg=bg, fg=fg)


class AeroButton(_AeroBase):
    def __init__(self, master, text="Button", command=None, width=160, height=40, radius=10, **kwargs):
        super().__init__(master, width, height, **kwargs)
        self.text = text
        self.command = command
        self.radius = radius
        self.hovered = False
        
        self.bind("<Enter>", lambda e: self._set_hover(True))
        self.bind("<Leave>", lambda e: self._set_hover(False))
        self.bind("<Button-1>", lambda e: self.command() if self.command else None)
        self.draw()

    def _set_hover(self, state):
        self.hovered = state
        self.draw()

    def draw(self):
        self.delete("all")
        self.configure(bg=self._get_parent_bg(), cursor="hand2")
        fill = self.colors["accent_hover"] if self.hovered else self.colors["accent"]
        self._round_rect(0, 0, self.w, self.h, self.radius, fill=fill, outline="")
        self.create_text(self.w/2, self.h/2, text=self.text, fill="#ffffff", font=("Segoe UI", 10, "bold"))

    def update_theme(self):
        self.draw()


class AeroEntry(_AeroBase):
    def __init__(self, master, placeholder="", width=220, height=38, radius=8, **kwargs):
        super().__init__(master, width, height, **kwargs)
        self.radius = radius
        self.placeholder = placeholder
        
        self.entry = tk.Entry(self, bd=0, highlightthickness=0, font=("Segoe UI", 10))
        self.create_window(width/2, height/2, window=self.entry, width=width-20, height=height-12)
        
        if placeholder:
            self._show_placeholder()
            self.entry.bind("<FocusIn>", self._clear_placeholder)
            self.entry.bind("<FocusOut>", self._restore_placeholder)
            
        self.draw()

    def _show_placeholder(self):
        self.entry.insert(0, self.placeholder)
        self.entry.configure(fg=self.colors["fg_muted"])
        self._has_placeholder = True

    def _clear_placeholder(self, e):
        if getattr(self, "_has_placeholder", False):
            self.entry.delete(0, tk.END)
            self.entry.configure(fg=self.colors["fg"])
            self._has_placeholder = False

    def _restore_placeholder(self, e):
        if not self.entry.get():
            self._show_placeholder()

    def get(self):
        if getattr(self, "_has_placeholder", False):
            return ""
        return self.entry.get()

    def draw(self):
        self.delete("bg_rect")
        self.configure(bg=self._get_parent_bg())
        self._round_rect(1, 1, self.w-1, self.h-1, self.radius, fill=self.colors["input_bg"], outline=self.colors["border"], tags="bg_rect")
        self.tag_lower("bg_rect")
        fg = self.colors["fg_muted"] if getattr(self, "_has_placeholder", False) else self.colors["fg"]
        self.entry.configure(bg=self.colors["input_bg"], fg=fg, insertbackground=self.colors["fg"])

    def update_theme(self):
        self.draw()


class AeroSwitch(_AeroBase):
    def __init__(self, master, command=None, initial=False, **kwargs):
        super().__init__(master, width=48, height=26, **kwargs)
        self.state = initial
        self.command = command
        self.bind("<Button-1>", self.toggle)
        self.draw()

    def toggle(self, e=None):
        self.state = not self.state
        self.draw()
        if self.command:
            self.command(self.state)

    def draw(self):
        self.delete("all")
        self.configure(bg=self._get_parent_bg(), cursor="hand2")
        bg_fill = self.colors["accent"] if self.state else self.colors["switch_off"]
        self._round_rect(0, 0, self.w, self.h, 13, fill=bg_fill, outline="")
        knob_x = self.w - 22 if self.state else 4
        self.create_oval(knob_x, 4, knob_x+18, 22, fill="#ffffff", outline="")

    def update_theme(self):
        self.draw()


class AeroCheckbox(_AeroBase):
    def __init__(self, master, text="Checkbox", command=None, initial=False, **kwargs):
        super().__init__(master, width=200, height=28, **kwargs)
        self.state = initial
        self.text = text
        self.command = command
        self.bind("<Button-1>", self.toggle)
        self.draw()

    def toggle(self, e=None):
        self.state = not self.state
        self.draw()
        if self.command:
            self.command(self.state)

    def get(self):
        return self.state

    def draw(self):
        self.delete("all")
        self.configure(bg=self._get_parent_bg(), cursor="hand2")
        
        # Kuţu (Box)
        box_fill = self.colors["accent"] if self.state else self.colors["input_bg"]
        self._round_rect(0, 4, 20, 24, 5, fill=box_fill, outline=self.colors["border"])
        
        if self.state:
            # Onay işareti (Check icon çizgileri)
            self.create_line(5, 14, 9, 18, fill="#ffffff", width=2, capstyle=tk.ROUND)
            self.create_line(9, 18, 15, 10, fill="#ffffff", width=2, capstyle=tk.ROUND)
            
        # Metin
        self.create_text(30, 14, text=self.text, anchor="w", fill=self.colors["fg"], font=("Segoe UI", 10))

    def update_theme(self):
        self.draw()


class AeroSlider(_AeroBase):
    def __init__(self, master, from_=0, to=100, command=None, width=200, height=24, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.from_ = from_
        self.to = to
        self.command = command
        self.value = from_
        
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<Button-1>", self._on_drag)
        self.draw()

    def _on_drag(self, e):
        # Koordinatı değere dönüştür
        x = max(10, min(e.x, self.w - 10))
        pct = (x - 10) / (self.w - 20)
        self.value = self.from_ + pct * (self.to - self.from_)
        self.draw()
        if self.command:
            self.command(round(self.value, 2))

    def get(self):
        return round(self.value, 2)

    def draw(self):
        self.delete("all")
        self.configure(bg=self._get_parent_bg(), cursor="hand2")
        
        # Ray (Track) arkaplanı
        self._round_rect(10, 10, self.w-10, 14, 2, fill=self.colors["switch_off"], outline="")
        
        # Dolu kısım
        pct = (self.value - self.from_) / (self.to - self.from_ or 1)
        fill_width = 10 + pct * (self.w - 20)
        if fill_width > 10:
            self._round_rect(10, 10, fill_width, 14, 2, fill=self.colors["accent"], outline="")
            
        # Topuz (Thumb)
        thumb_x = fill_width
        self.create_oval(thumb_x - 7, 3, thumb_x + 7, 21, fill="#ffffff", outline=self.colors["border"])

    def update_theme(self):
        self.draw()
