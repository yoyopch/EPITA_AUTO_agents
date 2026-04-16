# D1 — Outil d'interrogation du portefeuille financier stocké en PostgreSQL.
# Permet à l'agent de consulter les positions, calculer les PnL et identifier les actifs risqués.

import os
import psycopg2
import yfinance as yf
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


def consulter_portfolio(query: str = "") -> str:
    """
    Consulte le portefeuille financier stocké en base de données.
    Retourne les positions avec le cours actuel, le PnL et la valeur totale.
    Entrée : nom d'utilisateur (optionnel, par défaut 'demo').
    """
    utilisateur = query.strip() if query.strip() else "demo"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT symbole, quantite, prix_achat, date_achat FROM portfolio_positions WHERE utilisateur = %s",
            (utilisateur,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return f"Aucune position trouvée pour l'utilisateur '{utilisateur}'."

        result = f"=== PORTEFEUILLE DE {utilisateur.upper()} ===\n"
        valeur_totale = 0.0
        pnl_total = 0.0

        for symbole, quantite, prix_achat, date_achat in rows:
            prix_achat = float(prix_achat)
            try:
                ticker = yf.Ticker(symbole)
                info = ticker.info
                cours_actuel = info.get("currentPrice") or info.get("regularMarketPrice") or prix_achat
            except Exception:
                cours_actuel = prix_achat

            valeur_ligne = cours_actuel * quantite
            pnl = (cours_actuel - prix_achat) * quantite
            pnl_pct = ((cours_actuel - prix_achat) / prix_achat) * 100

            tendance = '📈' if pnl >= 0 else '📉'
            result += (
                f"  {symbole} : {quantite} x {cours_actuel:.2f} $ = {valeur_ligne:.2f} $ "
                f"| PnL : {pnl:+.2f} $ ({pnl_pct:+.1f}%) {tendance} "
                f"| Acheté le {date_achat}\n"
            )
            valeur_totale += valeur_ligne
            pnl_total += pnl

        result += f"\nValeur totale : {valeur_totale:,.2f} $"
        result += f"\nPnL total : {pnl_total:+,.2f} $"
        return result

    except Exception as e:
        return f"Erreur base de données : {e}"


def identifier_actifs_risques(query: str = "") -> str:
    """
    Identifie les actifs du portefeuille avec les plus fortes pertes (PnL négatif).
    Entrée : nom d'utilisateur (optionnel, par défaut 'demo').
    """
    utilisateur = query.strip() if query.strip() else "demo"
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT symbole, quantite, prix_achat FROM portfolio_positions WHERE utilisateur = %s",
            (utilisateur,)
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()

        if not rows:
            return f"Aucune position trouvée pour '{utilisateur}'."

        actifs = []
        for symbole, quantite, prix_achat in rows:
            prix_achat = float(prix_achat)
            try:
                ticker = yf.Ticker(symbole)
                info = ticker.info
                cours_actuel = info.get("currentPrice") or info.get("regularMarketPrice") or prix_achat
            except Exception:
                cours_actuel = prix_achat

            pnl = (cours_actuel - prix_achat) * quantite
            pnl_pct = ((cours_actuel - prix_achat) / prix_achat) * 100
            actifs.append((symbole, quantite, pnl, pnl_pct))

        # Trier par PnL croissant (les plus en perte d'abord)
        actifs.sort(key=lambda x: x[2])
        result = "=== ACTIFS LES PLUS RISQUÉS ===\n"
        for symbole, quantite, pnl, pnl_pct in actifs:
            statut = "⚠️ EN PERTE" if pnl < 0 else "✅ EN GAIN"
            result += f"  {symbole} ({quantite} parts) : PnL {pnl:+.2f} $ ({pnl_pct:+.1f}%) {statut}\n"
        return result

    except Exception as e:
        return f"Erreur : {e}"


if __name__ == "__main__":
    print("=== Test consulter_portfolio ===")
    print(consulter_portfolio("demo"))
    print("\n=== Test identifier_actifs_risques ===")
    print(identifier_actifs_risques("demo"))
