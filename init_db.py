"""
Script d'initialisation de la base de données PostgreSQL.
Crée les tables clients et produits, puis insère les données initiales.
Usage : python init_db.py
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
    """Crée les tables clients et produits."""
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id VARCHAR(10) PRIMARY KEY,
            nom VARCHAR(100) NOT NULL,
            email VARCHAR(100),
            ville VARCHAR(50),
            solde_compte NUMERIC(12, 2) NOT NULL DEFAULT 0,
            type_compte VARCHAR(20) NOT NULL DEFAULT 'Standard',
            date_inscription DATE,
            achats_total NUMERIC(12, 2) DEFAULT 0
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS produits (
            id VARCHAR(10) PRIMARY KEY,
            nom VARCHAR(100) NOT NULL,
            prix_ht NUMERIC(10, 2) NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0
        );
    """)


def inserer_donnees(cur):
    """Insère les données initiales (mêmes que les dictionnaires du TP)."""
    # -- Clients
    clients = [
        ("C001", "Marie Dupont", "marie.dupont@email.fr", "Paris", 15420.50, "Premium", "2021-03-15", 8750.00),
        ("C002", "Jean Martin", None, None, 3200.00, "Standard", None, 0),
        ("C003", "Sophie Bernard", None, None, 28900.00, "VIP", None, 0),
        ("C004", "Lucas Petit", None, None, 750.00, "Standard", None, 0),
    ]
    for c in clients:
        cur.execute("""
            INSERT INTO clients (id, nom, email, ville, solde_compte, type_compte, date_inscription, achats_total)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, c)

    # -- Produits
    produits = [
        ("P001", "Ordinateur portable Pro", 899.00, 45),
        ("P002", "Souris ergonomique", 49.90, 120),
        ("P003", "Bureau réglable", 350.00, 18),
        ("P004", "Casque audio sans fil", 129.00, 67),
        ("P005", "Écran 27 pouces 4K", 549.00, 30),
    ]
    for p in produits:
        cur.execute("""
            INSERT INTO produits (id, nom, prix_ht, stock)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
        """, p)


if __name__ == "__main__":
    print("Connexion à PostgreSQL...")
    conn = get_connection()
    cur = conn.cursor()

    print("Création des tables...")
    creer_tables(cur)

    print("Insertion des données initiales...")
    inserer_donnees(cur)

    conn.commit()
    cur.close()
    conn.close()
    print("Base de données initialisée avec succès !")
