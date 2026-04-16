"""
Script d'initialisation des tables portfolio dans PostgreSQL.
Crée la table portfolio_positions et insère des données de démonstration.
Usage : python init_portfolio_db.py
"""

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
    return psycopg2.connect(**DB_CONFIG)


def creer_tables(cur):
    """Crée les tables pour le portefeuille financier."""
    cur.execute("""
        CREATE TABLE IF NOT EXISTS portfolio_positions (
            id SERIAL PRIMARY KEY,
            utilisateur VARCHAR(50) NOT NULL DEFAULT 'demo',
            symbole VARCHAR(10) NOT NULL,
            quantite INTEGER NOT NULL,
            prix_achat NUMERIC(12, 2) NOT NULL,
            date_achat DATE NOT NULL DEFAULT CURRENT_DATE
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS portfolio_transactions (
            id SERIAL PRIMARY KEY,
            utilisateur VARCHAR(50) NOT NULL DEFAULT 'demo',
            symbole VARCHAR(10) NOT NULL,
            type_operation VARCHAR(10) NOT NULL,
            quantite INTEGER NOT NULL,
            prix NUMERIC(12, 2) NOT NULL,
            date_transaction TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """)


def inserer_donnees_demo(cur):
    """Insère des positions de démonstration (vide les données demo avant pour éviter les doublons)."""
    cur.execute("DELETE FROM portfolio_transactions WHERE utilisateur = 'demo'")
    cur.execute("DELETE FROM portfolio_positions WHERE utilisateur = 'demo'")

    positions = [
        ("demo", "AAPL", 10, 150.00, "2024-01-15"),
        ("demo", "MSFT", 5, 380.00, "2024-02-20"),
        ("demo", "TSLA", 8, 200.00, "2024-03-10"),
        ("demo", "GOOGL", 3, 140.00, "2024-04-05"),
    ]
    for p in positions:
        cur.execute("""
            INSERT INTO portfolio_positions (utilisateur, symbole, quantite, prix_achat, date_achat)
            VALUES (%s, %s, %s, %s, %s);
        """, p)

    transactions = [
        ("demo", "AAPL", "ACHAT", 10, 150.00),
        ("demo", "MSFT", "ACHAT", 5, 380.00),
        ("demo", "TSLA", "ACHAT", 8, 200.00),
        ("demo", "GOOGL", "ACHAT", 3, 140.00),
    ]
    for t in transactions:
        cur.execute("""
            INSERT INTO portfolio_transactions (utilisateur, symbole, type_operation, quantite, prix)
            VALUES (%s, %s, %s, %s, %s);
        """, t)


if __name__ == "__main__":
    print("Connexion à PostgreSQL...")
    conn = get_connection()
    cur = conn.cursor()

    print("Création des tables portfolio...")
    creer_tables(cur)

    print("Insertion des données de démonstration...")
    inserer_donnees_demo(cur)

    conn.commit()
    cur.close()
    conn.close()
    print("Tables portfolio initialisées avec succès !")
