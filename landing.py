
import tkinter as tk
from tkinter import ttk, messagebox

NAVY = "#05051A"
PANEL = "#0F172A"
SECONDARY = "#1A2B50"
CYAN = "#00F2FF"
PURPLE = "#BC00FF"
WHITE = "#F8FAFC"
MUTED = "#A7B4CC"
GREEN = "#22C55E"
ORANGE = "#F59E0B"
RED = "#EF4444"
FONT = "Segoe UI"


def configure_window(window, title, geometry="1200x720", minsize=(900, 600)):
    window.title(title)
    window.geometry(geometry)
    window.minsize(*minsize)
    window.configure(bg=NAVY)


def style_progressbars(root):
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "Skillora.Horizontal.TProgressbar",
        troughcolor=SECONDARY,
        background=CYAN,
        bordercolor=SECONDARY,
        lightcolor=CYAN,
        darkcolor=CYAN,
        thickness=9
    )


def make_button(parent, text, command, primary=True, width=None):
    bg = CYAN if primary else SECONDARY
    fg = NAVY if primary else WHITE

    button = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        fg=fg,
        activebackground="#8AFAFF" if primary else "#29436E",
        activeforeground=NAVY if primary else WHITE,
        relief="flat",
        bd=0,
        cursor="hand2",
        font=(FONT, 10, "bold"),
        padx=18,
        pady=10,
        width=width
    )

    hover = "#8AFAFF" if primary else "#29436E"

    button.bind("<Enter>", lambda event: button.configure(bg=hover))
    button.bind("<Leave>", lambda event: button.configure(bg=bg))

    return button


def make_card(parent, padding=18):
    return tk.Frame(
        parent,
        bg=PANEL,
        highlightthickness=1,
        highlightbackground="#243451",
        padx=padding,
        pady=padding
    )


class LandingPage(tk.Frame):
    """Page d'accueil Skillora. on_login est le callback vers Login."""

    def __init__(self, master, on_login=None, on_catalog=None, **kwargs):
        super().__init__(master, bg=NAVY, **kwargs)

        self.on_login = on_login
        self.on_catalog = on_catalog

        self._build()

    def _build(self):
        nav = tk.Frame(self, bg=NAVY, padx=48, pady=22)
        nav.pack(fill="x")

        brand = tk.Frame(nav, bg=NAVY)
        brand.pack(side="left")

        self._logo(brand, size=34)

        tk.Label(
            brand,
            text="SKILLORA",
            bg=NAVY,
            fg=WHITE,
            font=(FONT, 18, "bold")
        ).pack(side="left", padx=(10, 0))

        links = tk.Frame(nav, bg=NAVY)
        links.pack(side="right")

        for label, callback in (
            ("Accueil", None),
            ("Formations", self._browse),
            ("À propos", self._about),
        ):
            tk.Button(
                links,
                text=label,
                command=callback,
                bg=NAVY,
                fg=MUTED,
                activebackground=NAVY,
                activeforeground=CYAN,
                relief="flat",
                bd=0,
                cursor="hand2",
                font=(FONT, 10)
            ).pack(side="left", padx=13)

        make_button(
            links,
            "Connexion",
            self._login,
            primary=True
        ).pack(side="left", padx=(16, 0))

        tk.Frame(
            self,
            bg="#243451",
            height=1
        ).pack(fill="x", padx=48)
        content = tk.Frame(
            self,
            bg=NAVY,
            padx=58,
            pady=35
        )

        content.pack(fill="both", expand=True)

        content.grid_columnconfigure(0, weight=6)
        content.grid_columnconfigure(1, weight=5)
        content.grid_rowconfigure(0, weight=1)

        left = tk.Frame(content, bg=NAVY)

        left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 22),
            pady=22
        )

        tk.Label(
            left,
            text="VOTRE AVENIR COMMENCE ICI",
            bg=NAVY,
            fg=CYAN,
            font=(FONT, 10, "bold")
        ).pack(anchor="w", pady=(12, 18))

        tk.Label(
            left,
            text="Learn more.",
            bg=NAVY,
            fg=WHITE,
            font=(FONT, 36, "bold")
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Become more.",
            bg=NAVY,
            fg=CYAN,
            font=(FONT, 36, "bold")
        ).pack(anchor="w")

        slogan = tk.Frame(left, bg=NAVY)
        slogan.pack(anchor="w", pady=(18, 18))

        for word in ("LEARN.", " DEVELOP.", " ACHIEVE."):
            tk.Label(
                slogan,
                text=word,
                bg=NAVY,
                fg=PURPLE if word.strip() == "ACHIEVE." else CYAN,
                font=(FONT, 12, "bold")
            ).pack(side="left")

        description = (
            "Skillora vous accompagne dans votre apprentissage. "
            "Explorez des formations de qualité, développez de nouvelles "
            "compétences et atteignez vos objectifs."
        )

        tk.Label(
            left,
            text=description,
            bg=NAVY,
            fg=MUTED,
            font=(FONT, 12),
            justify="left",
            wraplength=470
        ).pack(anchor="w", pady=(0, 26))

        actions = tk.Frame(left, bg=NAVY)
        actions.pack(anchor="w")

        make_button(
            actions,
            "Get Started  →",
            self._login
        ).pack(side="left", padx=(0, 12))

        make_button(
            actions,
            "Explore courses",
            self._browse,
            primary=False
        ).pack(side="left")

        tk.Label(
            left,
            text="Apprenez à votre rythme. Progressez chaque jour.",
            bg=NAVY,
            fg="#71819E",
            font=(FONT, 9)
        ).pack(anchor="w", pady=(18, 0))
        right = tk.Frame(content, bg=NAVY)

        right.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self._draw_illustration(right)
        footer = tk.Frame(
            self,
            bg=NAVY,
            padx=58,
            pady=0
        )
        footer.pack(
            fill="x",
            pady=(0, 24)
        )

        tk.Frame(
            footer,
            bg="#243451",
            height=1
        ).pack(fill="x", pady=(0, 18))

        features = [
            ("▣", "Quality Courses", "Des formations adaptées"),
            ("↗", "Track Progress", "Suivez votre évolution"),
            ("★", "Achieve More", "Atteignez vos objectifs"),
        ]

        for index, (symbol, title, subtitle) in enumerate(features):

            item = tk.Frame(footer, bg=NAVY)

            item.pack(
                side="left",
                expand=True,
                fill="x",
                padx=(0 if index == 0 else 16, 12)
            )

            tk.Label(
                item,
                text=symbol,
                bg=NAVY,
                fg=CYAN if index != 2 else ORANGE,
                font=(FONT, 22, "bold")
            ).pack(side="left", padx=(0, 12))

            texts = tk.Frame(item, bg=NAVY)
            texts.pack(side="left")

            tk.Label(
                texts,
                text=title,
                bg=NAVY,
                fg=WHITE,
                font=(FONT, 10, "bold")
            ).pack(anchor="w")

            tk.Label(
                texts,
                text=subtitle,
                bg=NAVY,
                fg=MUTED,
                font=(FONT, 9)
            ).pack(anchor="w", pady=(3, 0))
    def _logo(self, parent, size=34):

        canvas = tk.Canvas(
            parent,
            width=size,
            height=size,
            bg=NAVY,
            highlightthickness=0
        )

        canvas.pack(side="left")

        cx = size / 2

        canvas.create_polygon(
            cx, 2,
            size-2, size*0.36,
            cx, size*0.7,
            2, size*0.36,
            fill=CYAN,
            outline=CYAN
        )

        canvas.create_polygon(
            cx, size*0.72,
            size-5, size*0.45,
            size-7, size*0.69,
            cx, size-2,
            fill=PURPLE,
            outline=PURPLE
        )
    def _draw_illustration(self, parent):

        canvas = tk.Canvas(
            parent,
            bg=NAVY,
            highlightthickness=0,
            width=480,
            height=390
        )

        canvas.pack(
            fill="both",
            expand=True,
            pady=12
        )
        canvas.create_oval(
            55, 25, 425, 385,
            outline="#102C59",
            width=2
        )

        canvas.create_oval(
            82, 52, 398, 358,
            outline="#172D55",
            width=2
        )

        canvas.create_arc(
            55, 75, 425, 365,
            start=195,
            extent=150,
            style="arc",
            outline=CYAN,
            width=3
        )

        canvas.create_arc(
            75, 55, 405, 345,
            start=15,
            extent=145,
            style="arc",
            outline=PURPLE,
            width=3
        )
        canvas.create_polygon(
            135, 105,
            330, 105,
            350, 250,
            155, 250,
            fill="#142B55",
            outline=CYAN,
            width=3
        )

        canvas.create_polygon(
            145, 115,
            320, 115,
            337, 239,
            164, 239,
            fill="#07132D",
            outline="#31558C",
            width=1
        )

        self._draw_cap(canvas, 205, 145, 270, 205)

        canvas.create_text(
            242, 222,
            text="SKILLORA",
            fill=WHITE,
            font=(FONT, 12, "bold")
        )
        canvas.create_polygon(
            155, 255,
            350, 255,
            395, 285,
            105, 285,
            fill="#1A2B50",
            outline="#54719F",
            width=2
        )

        canvas.create_line(
            105, 285,
            395, 285,
            fill="#6B83B3",
            width=2
        )

        canvas.create_polygon(
            210, 258,
            265, 258,
            275, 269,
            200, 269,
            fill="#15294D",
            outline="#3A5B8D"
        )
        self._floating_card(
            canvas, 20, 105, 105, 160, "▶", CYAN
        )

        self._floating_card(
            canvas, 365, 75, 450, 130, "✦", PURPLE
        )

        self._floating_card(
            canvas, 355, 300, 440, 355, "✓", GREEN
        )
    def _draw_cap(self, canvas, x1, y1, x2, y2):

        middle = (x1 + x2) / 2

        canvas.create_polygon(
            middle, y1,
            x2, (y1+y2)/2,
            middle, y2-5,
            x1, (y1+y2)/2,
            fill=CYAN,
            outline="#56FFFF",
            width=1
        )

        canvas.create_line(
            x2-4, (y1+y2)/2,
            x2-4, y2+5,
            fill=ORANGE,
            width=2
        )

        canvas.create_oval(
            x2-7, y2+3,
            x2-1, y2+9,
            fill=ORANGE,
            outline=ORANGE
        )
    def _floating_card(self, canvas, x1, y1, x2, y2, symbol, color):

        canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=PANEL,
            outline="#29436E",
            width=2
        )

        canvas.create_text(
            (x1+x2)/2,
            (y1+y2)/2,
            text=symbol,
            fill=color,
            font=(FONT, 21, "bold")
        )
    def _login(self):

        if callable(self.on_login):
            self.on_login()

        else:
            messagebox.showinfo(
                "Skillora",
                "Reliez ce bouton à la page Login depuis main.py."
            )
    def _browse(self):

        if callable(self.on_catalog):
            self.on_catalog()

        else:
            messagebox.showinfo(
                "Skillora",
                "Le catalogue sera accessible après connexion."
            )
    def _about(self):

        messagebox.showinfo(
            "À propos de Skillora",
            "Skillora est une plateforme de gestion et de suivi des formations."
        )

if __name__ == "__main__":

    root = tk.Tk()

    configure_window(
        root,
        "Skillora — Learn. Develop. Achieve."
    )

    page = LandingPage(root)

    page.pack(
        fill="both",
        expand=True
    )

    root.mainloop()
