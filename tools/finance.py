# Cet outil simule un flux de données financières en temps réel (cours d'actions, cryptomonnaies).
# Il génère des variations aléatoires pour simuler le comportement réel des marchés.

# A2 — Cours boursiers réels via yfinance (les actions utilisent maintenant des données réelles)

import random, datetime
import yfinance as yf

# Données simulées conservées en fallback
ACTIONS = {
    "AAPL":  { "nom": "Apple Inc.",       "prix_base": 182.50 },
    "MSFT":  { "nom": "Microsoft Corp.",   "prix_base": 415.20 },
    "GOOGL": { "nom": "Alphabet (Google)", "prix_base": 175.80 },
    "LVMH":  { "nom": "LVMH Moët Hennessy","prix_base": 750.00 },
    "TSLA":  { "nom": "Tesla Inc.",         "prix_base": 248.00 },
    "AIR":   { "nom": "Airbus SE",          "prix_base": 168.40 },
}

CRYPTOS = {
    "BTC": { "nom": "Bitcoin",  "prix_base": 67500.00 },
    "ETH": { "nom": "Ethereum", "prix_base": 3200.00  },
    "SOL": { "nom": "Solana",   "prix_base": 175.00   },
}


def obtenir_cours_action(symbole: str) -> str:
    """Retourne le cours réel d'une action via yfinance, avec fallback simulé."""
    symbole = symbole.strip().upper()
    try:
        ticker = yf.Ticker(symbole)
        info = ticker.info
        cours = info.get("currentPrice") or info.get("regularMarketPrice")
        if cours is None:
            raise ValueError("Cours non disponible")
        nom = info.get("shortName", symbole)
        prev_close = info.get("previousClose", cours)
        variation_pct = ((cours - prev_close) / prev_close) * 100 if prev_close else 0
        tendance = '📈' if variation_pct >= 0 else '📉'
        volume = info.get("volume", "N/A")
        return (f"{symbole} ({nom}) {tendance} : {cours:.2f} $ ({variation_pct:+.2f}%) "
                f"| Volume : {volume}")
    except Exception:
        # Fallback sur données simulées si yfinance échoue
        if symbole not in ACTIONS:
            return f"Action '{symbole}' non trouvée."
        action = ACTIONS[symbole]
        variation_pct = random.uniform(-3.0, 3.0)   # Variation aléatoire
        cours = action['prix_base'] * (1 + variation_pct / 100)
        tendance = '📈' if variation_pct >= 0 else '📉'
        return f"{symbole} {tendance} : {cours:.2f} $ ({variation_pct:+.2f}%) [données simulées]"


def obtenir_cours_crypto(symbole: str) -> str:
    """Retourne le cours simulé d'une cryptomonnaie avec sa variation (+/-5%)."""
    symbole = symbole.strip().upper()
    if symbole not in CRYPTOS:
        return f"Crypto '{symbole}' non trouvée."
    crypto = CRYPTOS[symbole]
    variation_pct = random.uniform(-5.0, 5.0)   # Variation aléatoire plus forte
    cours = crypto['prix_base'] * (1 + variation_pct / 100)
    tendance = '📈' if variation_pct >= 0 else '📉'
    return f"{symbole} {tendance} : {cours:.2f} $ ({variation_pct:+.2f}%)"


if __name__ == "__main__":
    print("=== Test obtenir_cours_action ===")
    for symbole in ["AAPL", "MSFT", "TSLA", "INCONNU"]:
        print(obtenir_cours_action(symbole))

    print("\n=== Test obtenir_cours_crypto ===")
    for symbole in ["BTC", "ETH", "SOL", "DOGE"]:
        print(obtenir_cours_crypto(symbole))
