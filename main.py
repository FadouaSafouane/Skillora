import tkinter as tk
from tkinter import messagebox

import database
import auth
import inscription_service

from landing import LandingPage
from login import LoginPage
from member_dashboard import MemberDashboard
from catalog import CatalogPage
from admin_dashboard import AdminDashboard


BG = "#05051A"
WHITE = "#F8FAFC"


class SkilloraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Skillora - Learn. Develop. Achieve.")
        self.root.geometry("1200x750")
        self.root.minsize(950, 600)
        self.root.configure(bg=BG)

        self.current_page = None
        self.current_member = None

        database.init_db()
        self.show_landing()

    def show_page(self, page_class, **kwargs):
        if self.current_page:
            self.current_page.destroy()

        self.current_page = page_class(self.root, **kwargs)
        self.current_page.pack(fill="both", expand=True)

    def show_landing(self):
        self.current_member = None

        self.show_page(
            LandingPage,
            on_login=self.show_login,
            on_catalog=self.show_public_catalog
        )

    def show_login(self):
        self.show_page(
            LoginPage,
            on_login=self.authenticate,
            on_back=self.show_landing
        )

    def authenticate(self, nom, prenom, code_apogee):
        membre = auth.authenticate(nom, prenom, code_apogee)

        if membre is None:
            messagebox.showerror(
                "Connexion impossible",
                "Informations incorrectes ou compte désactivé."
            )
            return

        self.current_member = membre

        role = str(membre.get("role", "")).strip().lower()

        if role == "admin":
            self.show_admin_dashboard()
        else:
            self.show_member_dashboard()

    def show_member_dashboard(self):
        if not self.current_member:
            self.show_login()
            return

        id_membre = self.current_member["id_membre"]

        self.show_page(
            MemberDashboard,
            member=self.current_member,
            get_stats=lambda: database.get_member_stats(id_membre),
            get_courses=lambda: database.get_member_courses(id_membre),
            on_browse_courses=self.show_catalog,
            on_logout=self.logout,
            on_view_details=self.show_catalog
        )

    def show_admin_dashboard(self):
        if not self.current_member:
            self.show_login()
            return

        self.show_page(
            AdminDashboard,
            member=self.current_member,
            on_logout=self.logout,
            on_back=self.show_landing
        )

    def show_catalog(self):
        if not self.current_member:
            self.show_login()
            return

        self.show_page(
            CatalogPage,
            member=self.current_member,
            on_back=self.show_member_dashboard,
            on_logout=self.logout,
            on_inscription=self.show_member_dashboard
        )

    def show_public_catalog(self):
        messagebox.showinfo(
            "Catalogue",
            "Connectez-vous pour consulter et rejoindre les formations."
        )
        self.show_login()

    def logout(self):
        self.current_member = None
        self.show_landing()


def main():
    root = tk.Tk()
    SkilloraApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()