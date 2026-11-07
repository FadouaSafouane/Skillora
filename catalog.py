import tkinter as tk
from tkinter import messagebox
import database
import inscription_service

BG = "#05051A"
PANEL = "#0F172A"
BLUE = "#1A2B50"
CYAN = "#00F2FF"
WHITE = "#F8FAFC"
GRAY = "#A7B4CC"


class CatalogPage(tk.Frame):
    def __init__(
        self,
        master,
        member=None,
        on_back=None,
        on_logout=None,
        on_inscription=None,
        **kwargs
    ):
        super().__init__(master, bg=BG, **kwargs)

        self.member = member or {}
        self.on_back = on_back
        self.on_logout = on_logout
        self.on_inscription = on_inscription

        self.create_interface()
        self.load_formations()

    def create_interface(self):
        header = tk.Frame(self, bg=PANEL, padx=25, pady=15)
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
            padx=12,
            pady=8
        ).pack(side="right")

        tk.Button(
            header,
            text="Retour",
            command=self.back,
            bg=BLUE,
            fg=WHITE,
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=8
        ).pack(side="right", padx=10)

        content = tk.Frame(self, bg=BG, padx=35, pady=25)
        content.pack(fill="both", expand=True)

        tk.Label(
            content,
            text="Catalogue des formations",
            fg=WHITE,
            bg=BG,
            font=("Segoe UI", 23, "bold")
        ).pack(anchor="w")

        tk.Label(
            content,
            text="Trouvez la formation qui correspond à vos objectifs.",
            fg=GRAY,
            bg=BG,
            font=("Segoe UI", 11)
        ).pack(anchor="w", pady=(5, 20))

        search_frame = tk.Frame(content, bg=BG)
        search_frame.pack(fill="x", pady=(0, 15))

        self.search_entry = tk.Entry(
            search_frame,
            bg=PANEL,
            fg=WHITE,
            insertbackground=WHITE,
            font=("Segoe UI", 11),
            relief="flat"
        )
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=10)
        self.search_entry.bind("<KeyRelease>", lambda event: self.load_formations())

        tk.Button(
            search_frame,
            text="Actualiser",
            command=self.load_formations,
            bg=CYAN,
            fg=BG,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            padx=15,
            pady=8
        ).pack(side="left", padx=10)

        self.canvas = tk.Canvas(
            content,
            bg=BG,
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(
            content,
            orient="vertical",
            command=self.canvas.yview
        )

        self.list_frame = tk.Frame(self.canvas, bg=BG)

        self.list_frame.bind(
            "<Configure>",
            lambda event: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.list_frame,
            anchor="nw"
        )

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.itemconfigure(
                self.canvas_window,
                width=event.width
            )
        )

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_formations(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        formations = database.get_all_formations(actives_seulement=True)
        recherche = self.search_entry.get().strip().lower()

        formations = [
            formation for formation in formations
            if recherche in str(formation.get("titre", "")).lower()
            or recherche in str(formation.get("technologie", "")).lower()
            or recherche in str(formation.get("description", "")).lower()
        ]

        if not formations:
            tk.Label(
                self.list_frame,
                text="Aucune formation disponible.",
                fg=GRAY,
                bg=BG,
                font=("Segoe UI", 11)
            ).pack(anchor="w", pady=20)
            return

        for formation in formations:
            self.create_course_card(formation)

    def create_course_card(self, formation):
        card = tk.Frame(
            self.list_frame,
            bg=PANEL,
            padx=22,
            pady=17,
            highlightbackground=BLUE,
            highlightthickness=1
        )
        card.pack(fill="x", pady=8, padx=5)

        tk.Label(
            card,
            text=formation.get("titre", ""),
            fg=WHITE,
            bg=PANEL,
            font=("Segoe UI", 15, "bold")
        ).pack(anchor="w")

        tk.Label(
            card,
            text=formation.get("technologie", ""),
            fg=CYAN,
            bg=PANEL,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=5)

        tk.Label(
            card,
            text=formation.get("description", ""),
            fg=GRAY,
            bg=PANEL,
            font=("Segoe UI", 10),
            wraplength=750,
            justify="left"
        ).pack(anchor="w", pady=5)

        inscrits = formation.get("inscrits", 0)
        capacite = formation.get("capacite", 0)
        duree = formation.get("duree_heures", 0)

        tk.Label(
            card,
            text=f"Durée : {duree} heures     Places : {inscrits}/{capacite}",
            fg=GRAY,
            bg=PANEL,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=5)

        tk.Button(
            card,
            text="S'inscrire",
            command=lambda f=formation: self.register(f),
            bg=CYAN,
            fg=BG,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            padx=18,
            pady=8
        ).pack(anchor="e", pady=(5, 0))

    def register(self, formation):
        id_membre = self.member.get("id_membre")

        if not id_membre:
            messagebox.showerror(
                "Erreur",
                "Impossible d'identifier votre compte."
            )
            return

        resultat = inscription_service.inscrire(
            id_membre,
            formation["id_formation"]
        )

        if resultat["succes"]:
            messagebox.showinfo("Inscription", resultat["message"])
            self.load_formations()

            if self.on_inscription:
                self.on_inscription()

        else:
            messagebox.showwarning("Inscription", resultat["message"])

    def back(self):
        if self.on_back:
            self.on_back()

    def logout(self):
        if self.on_logout:
            self.on_logout()