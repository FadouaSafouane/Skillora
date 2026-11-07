import database


def authenticate(nom, prenom, code_apogee):
    if not nom.strip() or not prenom.strip() or not str(code_apogee).strip():
        return None

    membre = database.get_member_by_credentials(
        nom.strip(),
        prenom.strip(),
        str(code_apogee).strip()
    )

    if membre is None:
        return None

    statut = str(membre.get("statut_acces", "")).strip().lower()

    if statut in ("banni", "non autorise", "non autorisé", "inactif", "bloque", "bloqué"):
        return None

    return membre


def verify_and_route(code_apogee):
    membre = database.get_member_by_apogee(code_apogee)

    if membre is None:
        return {
            "status": "error",
            "message": "Membre introuvable."
        }

    statut = str(membre.get("statut_acces", "")).strip().lower()

    if statut in ("banni", "non autorise", "non autorisé", "inactif"):
        return {
            "status": "denied",
            "message": "Ce compte est désactivé."
        }

    return {
        "status": "success",
        "role": membre.get("role", "Etudiant"),
        "member": membre
    }