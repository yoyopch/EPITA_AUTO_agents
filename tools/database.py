# Cet outil simule une base de données relationnelle contenant des informations sur les clients et les produits d'une PME.
# Il permet à l'agent de répondre à des questions du type :
# «Quel est le solde du compte de Marie Dupont ?» ou
# «Combien coûte le produit X ?»

# A1 — Migration vers PostgreSQL (les dictionnaires ont été remplacés par des requêtes SQL)

import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "langchain_db"),
    "user": os.getenv("DB_USER", "langchain"),
    "password": os.getenv("DB_PASSWORD", "langchain123"),
}


def get_connection():
    """Retourne une connexion à la base de données PostgreSQL."""
    return psycopg2.connect(**DB_CONFIG)


def rechercher_client(query: str) -> str:
    """Recherche un client par nom ou par identifiant."""
    query = query.strip()
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Recherche par ID
        cur.execute("SELECT id, nom, solde_compte, type_compte FROM clients WHERE UPPER(id) = %s", (query.upper(),))
        row = cur.fetchone()
        if row:
            cur.close()
            conn.close()
            return f"Client : {row[1]} | Solde : {row[2]:.2f} € | Type de compte : {row[3]}"
        # Recherche par nom (partiel, insensible à la casse)
        cur.execute("SELECT id, nom, solde_compte, type_compte FROM clients WHERE LOWER(nom) LIKE %s", (f"%{query.lower()}%",))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return f"Client : {row[1]} | Solde : {row[2]:.2f} € | Type de compte : {row[3]}"
        return f"Aucun client trouvé pour : '{query}'"
    except Exception as e:
        return f"Erreur base de données : {e}"


def rechercher_produit(query: str) -> str:
    """Recherche un produit par nom ou identifiant. Retourne prix HT, TVA, prix TTC, stock."""
    query = query.strip()
    try:
        conn = get_connection()
        cur = conn.cursor()
        # Recherche par ID
        cur.execute("SELECT id, nom, prix_ht, stock FROM produits WHERE UPPER(id) = %s", (query.upper(),))
        row = cur.fetchone()
        if not row:
            # Recherche par nom (partiel, insensible à la casse)
            cur.execute("SELECT id, nom, prix_ht, stock FROM produits WHERE LOWER(nom) LIKE %s", (f"%{query.lower()}%",))
            row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            prix_ht = float(row[2])
            tva = prix_ht * 0.20
            prix_ttc = prix_ht + tva
            return (f"Produit : {row[1]} | Prix HT : {prix_ht:.2f} € "
                    f"| TVA : {tva:.2f} € | Prix TTC : {prix_ttc:.2f} € | Stock : {row[3]}")
        return f"Aucun produit trouvé pour : '{query}'"
    except Exception as e:
        return f"Erreur base de données : {e}"


def lister_tous_les_clients(query: str = "") -> str:
    """Retourne la liste complète de tous les clients."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nom, type_compte, solde_compte FROM clients ORDER BY id")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        result = "Liste des clients :\n"
        for row in rows:
            result += f"  {row[0]} : {row[1]} | {row[2]} | Solde : {row[3]:.2f} €\n"
        return result
    except Exception as e:
        return f"Erreur base de données : {e}"


if __name__ == "__main__":
    print("=== Test rechercher_client ===")
    print(rechercher_client("Marie Dupont"))
    print(rechercher_client("C002"))
    print(rechercher_client("inconnu"))

    print("\n=== Test rechercher_produit ===")
    print(rechercher_produit("P001"))
    print(rechercher_produit("Souris"))
    print(rechercher_produit("inconnu"))

    print("\n=== Test lister_tous_les_clients ===")
    print(lister_tous_les_clients())
