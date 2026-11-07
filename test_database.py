import database

connexion = database.connect_db()

connexion.execute(
    """
    INSERT INTO etudiant
    (nom, prenom, code_apoge, role, statut_acces)
    VALUES (?, ?, ?, ?, ?)
    """,
    ("Test", "Etudiant", "12345", "Etudiant", "autorise")
)

connexion.execute(
    """
    INSERT INTO etudiant
    (nom, prenom, code_apoge, role, statut_acces)
    VALUES (?, ?, ?, ?, ?)
    """,
    ("Admin", "Skillora", "99999", "admin", "autorise")
)

connexion.execute(
    """
    INSERT INTO formation
    (titre, technologie, description, duree_heures, capacite, actif)
    VALUES (?, ?, ?, ?, ?, ?)
    """,
    ("Python débutant", "Python", "Apprendre les bases de Python.", 30, 20, "oui")
)

connexion.commit()
connexion.close()

print("Comptes et formation créés.")