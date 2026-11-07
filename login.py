import tkinter as tk
from tkinter import messagebox

BG = "#05051A"
PANEL = "#0F172A"
BLUE = "#1A2B50"
CYAN = "#00F2FF"
WHITE = "#F8FAFC"
GRAY = "#A7B4CC"


class LoginPage(tk.Frame):
    def __init__(self, master, on_login=None, on_back=None, **kwargs):
        super().__init__(master, bg=BG, **kwargs)

        self.on_login = on_login
        self.on_back = on_back

        self.create_interface()

    def create_interface(self):
        container = tk.Frame(self, bg=PANEL, padx=45, pady=35)
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            container,
            text="SKILLORA",
            font=("Segoe UI", 25, "bold"),
            fg=CYAN,
            bg=PANEL
        ).pack(pady=(0, 8))

        tk.Label(
            container,
            text="Connectez-vous à votre espace",
            font=("Segoe UI", 11),
            fg=GRAY,
            bg=PANEL
        ).pack(pady=(0, 25))

        tk.Label(
            container,
            text="Nom",
            fg=WHITE,
            bg=PANEL,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.nom_entry = tk.Entry(
            container,
            width=35,
            font=("Segoe UI", 11),
            bg=BLUE,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat"
        )
        self.nom_entry.pack(pady=(7, 17), ipady=9)

        tk.Label(
            container,
            text="Prénom",
            fg=WHITE,
            bg=PANEL,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.prenom_entry = tk.Entry(
            container,
            width=35,
            font=("Segoe UI", 11),
            bg=BLUE,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat"
        )
        self.prenom_entry.pack(pady=(7, 17), ipady=9)

        tk.Label(
            container,
            text="Code Apogée",
            fg=WHITE,
            bg=PANEL,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.code_entry = tk.Entry(
            container,
            width=35,
            font=("Segoe UI", 11),
            bg=BLUE,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            show="*"
        )
        self.code_entry.pack(pady=(7, 25), ipady=9)

        tk.Button(
            container,
            text="Se connecter",
            command=self.login,
            bg=CYAN,
            fg=BG,
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            cursor="hand2",
            width=30,
            pady=11
        ).pack()

        tk.Button(
            container,
            text="Retour",
            command=self.back,
            bg=PANEL,
            fg=GRAY,
            font=("Segoe UI", 10),
            relief="flat",
            cursor="hand2"
        ).pack(pady=(15, 0))

        self.code_entry.bind("<Return>", lambda event: self.login())

    def login(self):
        nom = self.nom_entry.get().strip()
        prenom = self.prenom_entry.get().strip()
        code = self.code_entry.get().strip()

        if not nom or not prenom or not code:
            messagebox.showwarning(
                "Champs manquants",
                "Veuillez remplir tous les champs."
            )
            return

        if self.on_login:
            self.on_login(nom, prenom, code)

    def back(self):
        if self.on_back:
            self.on_back()
