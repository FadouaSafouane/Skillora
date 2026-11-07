import tkinter as tk
from tkinter import messagebox, simpledialog
import database

BG = "#05051A"
PANEL = "#0F172A"
BLUE = "#1A2B50"
CYAN = "#00F2FF"
WHITE = "#F8FAFC"
GRAY = "#A7B4CC"
GREEN = "#22C55E"


class AdminDashboard(tk.Frame):
    def __init__(
        self,
        master,
        member=None,
        on_logout=None,
        on_back=None,
        **kwargs
    ):
        super().__init__(master, bg=BG, **kwargs)

        self.member = member or {}
        self.on_logout = on_logout
        self.on_back = on_back

        self.create_interface()

    def create_interface(self):
        header = tk.Frame(self, bg=PANEL, padx=25, pady=16)
        header.pack(fill="x")

        tk.Label(
            header,
            text="SKILLORA ADMIN",
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

        content = tk.Frame(self, bg=BG, padx=30, pady=25)
        content.pack(fill="both", expand=True)

        tk.Label(
            content,
            text="Tableau de bord administrateur",
            fg=WHITE,
            bg=BG,
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        tk.Label(
            content,
            text="Gestion des membres et des formations.",
            fg=GRAY,
            bg=BG,
            font=("Segoe UI", 11)
        ).pack(anchor="w", pady=(5, 20))

        stats = database.get_admin_stats()

        stats_frame = tk.Frame(content, bg=BG)
        stats_frame.pack(fill="x", pady=10)

        self.create_stat_card(stats_frame, "Membres", stats["membres"])
        self.create_stat_card(stats_frame, "Formations", stats["formations"])
        self.create_stat_card(stats_frame, "Inscriptions", stats["inscriptions"])

        actions = tk.Frame(content, bg=BG)
        actions.pack(fill="x", pady=20)

        tk.Button(
            actions,
            text="Actualiser",
            command=self.refresh_members,
            bg=CYAN,
            fg=BG,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            padx=15,
            pady=9
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            actions,
            text="Ajouter une formation",
            command=self.add_formation,
            bg=BLUE,
            fg=WHITE,
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=9
        ).pack(side="left")

        tk.Label(
            content,
            text="Liste des membres",
            fg=WHITE,
            bg=BG,
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", pady=(5, 10))

        table_frame = tk.Frame(content, bg=PANEL)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "nom", "prenom", "code", "role", "statut")

        self.table = tk.Frame(table_frame, bg=PANEL)
        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        headers = [
            ("ID", 5),
            ("Nom", 15),
            ("Prénom", 15),
            ("Code Apogée", 15),
            ("Rôle", 12),
            ("Statut", 15)
        ]

        for index, (label, width) in enumerate(headers):
            tk.Label(
                self.table,
                text=label,
                width=width,
                fg=CYAN,
                bg=PANEL,
                font=("Segoe UI", 9, "bold"),
                anchor="w"
            ).grid(row=0, column=index, padx=4, pady=8, sticky="w")

        self.refresh_members()

        buttons = tk.Frame(content, bg=BG)
        buttons.pack(fill="x", pady=12)

        tk.Button(
            buttons,
            text="Bannir le membre sélectionné",
            command=self.ban_member,
            bg="#7F1D1D",
            fg=WHITE,
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            buttons,
            text="Réactiver le membre sélectionné",
            command=self.activate_member,
            bg=GREEN,
            fg=BG,
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8
        ).pack(side="left")

    def create_stat_card(self, parent, title, value):
        card = tk.Frame(
            parent,
            bg=PANEL,
            padx=20,
            pady=15,
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
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", pady=(5, 0))

    def refresh_members(self):
        for widget in self.table.winfo_children():
            if int(widget.grid_info().get("row", 0)) > 0:
                widget.destroy()

        membres = database.get_all_members()

        for row, membre in enumerate(membres, start=1):
            valeurs = [
                membre["id_membre"],
                membre["nom"],
                membre["prenom"],
                membre["code_apoge"],
                membre["role"],
                membre["statut_acces"]
            ]

            for column, valeur in enumerate(valeurs):
                label = tk.Label(
                    self.table,
                    text=str(valeur),
                    fg=WHITE,
                    bg=PANEL,
                    font=("Segoe UI", 9),
                    anchor="w"
                )
                label.grid(
                    row=row,
                    column=column,
                    padx=4,
                    pady=6,
                    sticky="w"
                )

                label.bind(
                    "<Button-1>",
                    lambda event, m=membre: self.select_member(m)
                )

    def select_member(self, membre):
        self.selected_member = membre

    def ban_member(self):
        membre = getattr(self, "selected_member", None)

        if not membre:
            messagebox.showwarning(
                "Sélection",
                "Veuillez sélectionner un membre dans la liste."
            )
            return

        database.update_member_status(
            membre["id_membre"],
            "banni"
        )

        self.selected_member = None
        self.refresh_members()
        messagebox.showinfo("Compte", "Le membre a été banni.")

    def activate_member(self):
        membre = getattr(self, "selected_member", None)

        if not membre:
            messagebox.showwarning(
                "Sélection",
                "Veuillez sélectionner un membre dans la liste."
            )
            return

        database.update_member_status(
            membre["id_membre"],
            "autorise"
        )

        self.selected_member = None
        self.refresh_members()
        messagebox.showinfo("Compte", "Le membre a été réactivé.")

    def add_formation(self):
        titre = simpledialog.askstring(
            "Nouvelle formation",
            "Titre de la formation :",
            parent=self
        )

        if not titre or not titre.strip():
            return

        technologie = simpledialog.askstring(
            "Nouvelle formation",
            "Technologie :",
            parent=self
        )

        description = simpledialog.askstring(
            "Nouvelle formation",
            "Description :",
            parent=self
        )

        duree = simpledialog.askinteger(
            "Nouvelle formation",
            "Durée en heures :",
            parent=self,
            minvalue=1
        )

        capacite = simpledialog.askinteger(
            "Nouvelle formation",
            "Capacité maximale :",
            parent=self,
            minvalue=1
        )

        if not duree or not capacite:
            return

        try:
            database.ajouter_formation(
                titre.strip(),
                technologie or "",
                description or "",
                duree,
                capacite
            )

            messagebox.showinfo(
                "Formation",
                "La formation a été ajoutée."
            )

            self.refresh_dashboard()

        except Exception as erreur:
            messagebox.showerror("Erreur", str(erreur))

    def refresh_dashboard(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.create_interface()

    def logout(self):
        if self.on_logout:
            self.on_logout()