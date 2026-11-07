import tkinter as tk
from tkinter import messagebox

BG = "#05051A"
PANEL = "#0F172A"
BLUE = "#1A2B50"
CYAN = "#00F2FF"
WHITE = "#F8FAFC"
GRAY = "#A7B4CC"
GREEN = "#22C55E"


class MemberDashboard(tk.Frame):
    def __init__(
        self,
        master,
        member=None,
        get_stats=None,
        get_courses=None,
        on_browse_courses=None,
        on_logout=None,
        on_view_details=None,
        **kwargs
    ):
        super().__init__(master, bg=BG, **kwargs)

        self.member = member or {}
        self.get_stats = get_stats
        self.get_courses = get_courses
        self.on_browse_courses = on_browse_courses
        self.on_logout = on_logout
        self.on_view_details = on_view_details

        self.create_interface()

    def create_interface(self):
        header = tk.Frame(self, bg=PANEL, padx=25, pady=18)
        header.pack(fill="x")

        tk.Label(
            header,
            text="SKILLORA",
            fg=CYAN,
            bg=PANEL,
            font=("Segoe UI", 20, "bold")
        ).pack(side="left")

        tk.Button(
            header,
            text="Déconnexion",
            command=self.logout,
            bg=BLUE,
            fg=WHITE,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(side="right")

        content = tk.Frame(self, bg=BG, padx=35, pady=25)
        content.pack(fill="both", expand=True)

        nom = self.member.get("prenom", "")
        nom_complet = f"{nom} {self.member.get('nom', '')}".strip()

        tk.Label(
            content,
            text=f"Bienvenue, {nom_complet}",
            fg=WHITE,
            bg=BG,
            font=("Segoe UI", 23, "bold")
        ).pack(anchor="w")

        tk.Label(
            content,
            text="Voici un aperçu de votre apprentissage.",
            fg=GRAY,
            bg=BG,
            font=("Segoe UI", 11)
        ).pack(anchor="w", pady=(5, 20))

        stats = self.get_stats() if self.get_stats else {}

        stats_frame = tk.Frame(content, bg=BG)
        stats_frame.pack(fill="x", pady=10)

        self.create_stat_card(
            stats_frame,
            "Formations suivies",
            stats.get("formations_suivies", 0)
        )

        self.create_stat_card(
            stats_frame,
            "Formations terminées",
            stats.get("formations_terminees", 0)
        )

        self.create_stat_card(
            stats_frame,
            "Progression moyenne",
            f"{stats.get('progression_moyenne', 0)} %"
        )

        courses_header = tk.Frame(content, bg=BG)
        courses_header.pack(fill="x", pady=(25, 10))

        tk.Label(
            courses_header,
            text="Mes formations",
            fg=WHITE,
            bg=BG,
            font=("Segoe UI", 17, "bold")
        ).pack(side="left")

        tk.Button(
            courses_header,
            text="Explorer les formations",
            command=self.browse,
            bg=CYAN,
            fg=BG,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
            padx=12,
            pady=8
        ).pack(side="right")

        self.courses_frame = tk.Frame(content, bg=BG)
        self.courses_frame.pack(fill="both", expand=True)

        self.load_courses()

    def create_stat_card(self, parent, title, value):
        card = tk.Frame(
            parent,
            bg=PANEL,
            padx=22,
            pady=18,
            highlightbackground=BLUE,
            highlightthickness=1
        )
        card.pack(side="left", fill="x", expand=True, padx=(0, 12))

        tk.Label(
            card,
            text=title,
            fg=GRAY,
            bg=PANEL,
            font=("Segoe UI", 10)
        ).pack(anchor="w")

        tk.Label(
            card,
            text=str(value),
            fg=CYAN,
            bg=PANEL,
            font=("Segoe UI", 23, "bold")
        ).pack(anchor="w", pady=(8, 0))

    def load_courses(self):
        for widget in self.courses_frame.winfo_children():
            widget.destroy()

        courses = self.get_courses() if self.get_courses else []

        if not courses:
            tk.Label(
                self.courses_frame,
                text="Vous n'êtes inscrit à aucune formation.",
                fg=GRAY,
                bg=BG,
                font=("Segoe UI", 11)
            ).pack(anchor="w", pady=20)
            return

        for course in courses:
            card = tk.Frame(
                self.courses_frame,
                bg=PANEL,
                padx=18,
                pady=14
            )
            card.pack(fill="x", pady=7)

            tk.Label(
                card,
                text=course.get("titre", "Formation"),
                fg=WHITE,
                bg=PANEL,
                font=("Segoe UI", 13, "bold")
            ).pack(anchor="w")

            tk.Label(
                card,
                text=course.get("technologie", ""),
                fg=CYAN,
                bg=PANEL,
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=4)

            progression = course.get("progression", 0)

            tk.Label(
                card,
                text=f"Progression : {progression} %",
                fg=GREEN,
                bg=PANEL,
                font=("Segoe UI", 10)
            ).pack(anchor="w")

    def browse(self):
        if self.on_browse_courses:
            self.on_browse_courses()

    def logout(self):
        if self.on_logout:
            self.on_logout()