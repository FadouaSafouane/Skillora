import database


def verifier_et_inscrire(id_etudiant, id_formation, connexion_bd=None):
    connexion = connexion_bd or database.connect_db()
    fermer_connexion = connexion_bd is None

    try:
        formation = connexion.execute(
            """
            SELECT id_formation, titre, capacite, actif
            FROM formation
            WHERE id_formation = ?
            """,
            (id_formation,)
        ).fetchone()

        if formation is None:
            return {
                "succes": False,
                "message": "Cette formation n'existe pas."
            }

        if str(formation["actif"]).lower() != "oui":
            return {
                "succes": False,
                "message": "Cette formation n'est plus disponible."
            }

        deja_inscrit = connexion.execute(
            """
            SELECT id_inscription
            FROM inscription
            WHERE id_membre = ? AND id_formation = ?
            """,
            (id_etudiant, id_formation)
        ).fetchone()

        if deja_inscrit:
            return {
                "succes": False,
                "message": "Vous êtes déjà inscrit à cette formation."
            }

        nombre_inscrits = connexion.execute(
            """
            SELECT COUNT(*)
            FROM inscription
            WHERE id_formation = ?
            """,
            (id_formation,)
        ).fetchone()[0]

        if nombre_inscrits >= formation["capacite"]:
            return {
                "succes": False,
                "message": "Cette formation a atteint sa capacité maximale."
            }

        connexion.execute(
            """
            INSERT INTO inscription
            (id_membre, id_formation, date_inscription, statut, progression)
            VALUES (?, ?, CURRENT_DATE, 'Inscrit', 0)
            """,
            (id_etudiant, id_formation)
        )

        connexion.commit()

        return {
            "succes": True,
            "message": "Votre inscription a été effectuée avec succès."
        }

    except Exception as erreur:
        connexion.rollback()

        return {
            "succes": False,
            "message": str(erreur)
        }

    finally:
        if fermer_connexion:
            connexion.close()


def inscrire(id_etudiant, id_formation):
    return verifier_et_inscrire(id_etudiant, id_formation)