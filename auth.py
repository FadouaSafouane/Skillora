# auth.py
# Fichier logique 

class AuthSystem:
    def __init__(self, database):
        """Initialise le système avec une instance de la base de données"""
        self.db = database

    def verify_and_route(self, apogee_code):
        """
        Vérifie l'identité, le rôle et le statut du membre pour l'orienter.
        Retourne un dictionnaire avec le statut de la requête et l'action à mener.
        """
        # Récupération du membre via son code Apogée unique
        member = self.db.get_member_by_apogee(apogee_code)
        
        if not member:
            return {"status": "error", "message": "Membre introuvable."}
            
        # 1. Vérifier si le membre est banni
        if member["statut"] == "Banni":
            return {
                "status": "denied", 
                "message": "Accès refusé : Votre compte a été banni ."
            }
            
        # 2. Identifier le rôle et orienter l'utilisateur
        if member["role"] == "admin":
            return {
                "status": "success", 
                "role": "admin", 
                "action": "Ouvrir le tableau de bord administrateur (ui/admin_dashboard.py)"
            }
        elif member["role"] == "membre":
            return {
                "status": "success", 
                "role": "membre", 
                "action": "Ouvrir le tableau de bord étudiant"
            }
            
        return {"status": "error", "message": "Rôle utilisateur inconnu."}
