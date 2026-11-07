import sqlite3
db=sqlite3.connect("application.db")
db.execute("PRAGMA foreign_keys = ON")
db.execute("create table if not exists etudiant( id_membre integer PRIMARY KEY, nom text, prenom text, code_apoge integer NOT NULL, role text, statut_acces text, CONSTRAINT etudiant_code_apoge_uk UNIQUE(code_apoge))")
db.execute("create table if not exists formation( id_formation integer PRIMARY KEY, titre text, technologie text, description text, duree_heures integer, capacite integer, actif text,CONSTRAINT formation_capacite_ck CHECK (capacite > 0))")
db.execute("create table if not exists inscription( id_inscription integer PRIMARY KEY, id_membre integer, id_formation integer, date_inscription date, statut text, score integer, progression integer, FOREIGN KEY (id_membre) REFERENCES etudiant(id_membre), FOREIGN KEY (id_formation) REFERENCES formation(id_formation),CONSTRAINT insc_code_uk UNIQUE(id_membre, id_formation),CONSTRAINT inscription_progression_ck CHECK (progression between 0 and 100))")
db.commit()
db.close()
