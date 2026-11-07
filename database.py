import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("application.db")


def connect_db():
    connexion = sqlite3.connect(DB_PATH)
    connexion.row_factory = sqlite3.Row
    connexion.execute("PRAGMA foreign_keys = ON")
    return connexion


def init_db():
    connexion = connect_db()

    connexion.executescript("""
        CREATE TABLE IF NOT EXISTS etudiant (
            id_membre INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prenom TEXT NOT NULL,
            code_apoge TEXT NOT NULL UNIQUE,
            role TEXT NOT NULL DEFAULT 'Etudiant',
            statut_acces TEXT NOT NULL DEFAULT 'autorise'
        );

        CREATE TABLE IF NOT EXISTS formation (
            id_formation INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            technologie TEXT,
            description TEXT,
            duree_heures INTEGER DEFAULT 0,
            capacite INTEGER DEFAULT 20,
            actif TEXT DEFAULT 'oui'
        );

        CREATE TABLE IF NOT EXISTS inscription (
            id_inscription INTEGER PRIMARY KEY AUTOINCREMENT,
            id_membre INTEGER NOT NULL,
            id_formation INTEGER NOT NULL,
            date_inscription TEXT DEFAULT CURRENT_DATE,
            statut TEXT DEFAULT 'Inscrit',
            score INTEGER DEFAULT 0,
            progression INTEGER DEFAULT 0,
            FOREIGN KEY (id_membre) REFERENCES etudiant(id_membre),
            FOREIGN KEY (id_formation) REFERENCES formation(id_formation),
            UNIQUE(id_membre, id_formation),
            CHECK(progression BETWEEN 0 AND 100)
        );
    """)

    connexion.commit()
    connexion.close()


def get_member_by_apogee(code_apogee):
    connexion = connect_db()
    membre = connexion.execute(
        "SELECT * FROM etudiant WHERE code_apoge = ?",
        (str(code_apogee),)
    ).fetchone()
    connexion.close()
    return dict(membre) if membre else None


def get_member_by_credentials(nom, prenom, code_apogee):
    connexion = connect_db()

    membre = connexion.execute(
        """
        SELECT * FROM etudiant
        WHERE LOWER(TRIM(nom)) = LOWER(TRIM(?))
        AND LOWER(TRIM(prenom)) = LOWER(TRIM(?))
        AND CAST(code_apoge AS TEXT) = ?
        """,
        (nom, prenom, str(code_apogee).strip())
    ).fetchone()

    connexion.close()
    return dict(membre) if membre else None


def get_member_stats(id_membre):
    connexion = connect_db()

    stats = connexion.execute(
        """
        SELECT
            COUNT(*) AS formations_suivies,
            SUM(CASE WHEN i.progression = 100 THEN 1 ELSE 0 END)
                AS formations_terminees,
            COALESCE(ROUND(AVG(i.progression), 0), 0)
                AS progression_moyenne
        FROM inscription i
        WHERE i.id_membre = ?
        """,
        (id_membre,)
    ).fetchone()

    connexion.close()

    return {
        "formations_suivies": stats["formations_suivies"] or 0,
        "formations_terminees": stats["formations_terminees"] or 0,
        "progression_moyenne": stats["progression_moyenne"] or 0
    }


def get_member_courses(id_membre):
    connexion = connect_db()

    formations = connexion.execute(
        """
        SELECT
            f.id_formation,
            f.titre,
            f.technologie,
            f.description,
            f.duree_heures,
            i.progression,
            i.statut
        FROM inscription i
        JOIN formation f ON f.id_formation = i.id_formation
        WHERE i.id_membre = ?
        ORDER BY i.date_inscription DESC
        """,
        (id_membre,)
    ).fetchall()

    connexion.close()
    return [dict(formation) for formation in formations]


def get_all_members():
    connexion = connect_db()

    membres = connexion.execute(
        """
        SELECT id_membre, nom, prenom, code_apoge, role, statut_acces
        FROM etudiant
        ORDER BY id_membre DESC
        """
    ).fetchall()

    connexion.close()
    return [dict(membre) for membre in membres]


def update_member_status(id_membre, statut):
    connexion = connect_db()

    connexion.execute(
        "UPDATE etudiant SET statut_acces = ? WHERE id_membre = ?",
        (statut, id_membre)
    )

    connexion.commit()
    connexion.close()


def get_all_formations(actives_seulement=False):
    connexion = connect_db()

    requete = """
        SELECT
            f.id_formation,
            f.titre,
            f.technologie,
            f.description,
            f.duree_heures,
            f.capacite,
            f.actif,
            COUNT(i.id_inscription) AS inscrits
        FROM formation f
        LEFT JOIN inscription i ON i.id_formation = f.id_formation
    """

    if actives_seulement:
        requete += " WHERE LOWER(f.actif) = 'oui'"

    requete += " GROUP BY f.id_formation ORDER BY f.id_formation DESC"

    formations = connexion.execute(requete).fetchall()
    connexion.close()

    return [dict(formation) for formation in formations]


def ajouter_formation(titre, technologie, description, duree_heures, capacite):
    connexion = connect_db()

    connexion.execute(
        """
        INSERT INTO formation
        (titre, technologie, description, duree_heures, capacite, actif)
        VALUES (?, ?, ?, ?, ?, 'oui')
        """,
        (titre, technologie, description, duree_heures, capacite)
    )

    connexion.commit()
    connexion.close()


def modifier_statut_formation(id_formation, actif):
    connexion = connect_db()

    connexion.execute(
        "UPDATE formation SET actif = ? WHERE id_formation = ?",
        (actif, id_formation)
    )

    connexion.commit()
    connexion.close()


def get_admin_stats():
    connexion = connect_db()

    membres = connexion.execute(
        "SELECT COUNT(*) FROM etudiant"
    ).fetchone()[0]

    formations = connexion.execute(
        "SELECT COUNT(*) FROM formation"
    ).fetchone()[0]

    inscriptions = connexion.execute(
        "SELECT COUNT(*) FROM inscription"
    ).fetchone()[0]

    connexion.close()

    return {
        "membres": membres,
        "formations": formations,
        "inscriptions": inscriptions
    }


init_db()

