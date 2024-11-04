import sqlite3 as sqlite

# Connexion à la base de données
conn = sqlite.connect("./database.db")

# Ajouter une nouvelle colonne 'id' à la table existante
conn.execute("ALTER TABLE movie ADD COLUMN recommended BOOLEAN DEFAULT FALSE;")
conn.execute("ALTER TABLE movie ADD COLUMN watched BOOLEAN DEFAULT FALSE;")


# Mettre à jour la colonne 'id' pour qu'elle contienne des valeurs uniques
#conn.execute("UPDATE movie SET id = rowid")

# Vérifier les résultats
cursor = conn.cursor()
for row in cursor.execute("SELECT * FROM movie LIMIT 10"):
    print(row)

# Fermer la connexion
conn.commit()  # N'oubliez pas de valider les changements
conn.close()
