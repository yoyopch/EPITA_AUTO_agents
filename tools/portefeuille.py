# B1 — Outil de calcul de la valeur d'un portefeuille boursier.
# Utilise yfinance pour récupérer les cours réels et calculer la valeur totale.

import yfinance as yf


def calculer_portefeuille(input_str: str) -> str:
    """
    Calcule la valeur d'un portefeuille boursier.
    Entrée : "SYMBOLE1:QUANTITE1|SYMBOLE2:QUANTITE2"
    Exemple : "AAPL:10|MSFT:5|TSLA:3"
    """
    positions = input_str.strip().split('|')
    valeur_totale = 0.0
    variation_totale = 0.0
    lignes = []

    for pos in positions:
        parts = pos.strip().split(':')
        if len(parts) != 2:
            lignes.append(f"  Format invalide : '{pos}' (attendu SYMBOLE:QUANTITE)")
            continue
        symbole = parts[0].strip().upper()
        try:
            quantite = int(parts[1].strip())
        except ValueError:
            lignes.append(f"  Quantité invalide pour {symbole}")
            continue

        try:
            ticker = yf.Ticker(symbole)
            info = ticker.info
            cours = info.get("currentPrice") or info.get("regularMarketPrice")
            if cours is None:
                lignes.append(f"  {symbole} : cours non disponible")
                continue
            prev_close = info.get("previousClose", cours)
            valeur_ligne = cours * quantite
            variation_pct = ((cours - prev_close) / prev_close) * 100 if prev_close else 0
            tendance = '📈' if variation_pct >= 0 else '📉'
            lignes.append(
                f"  {symbole} : {quantite} x {cours:.2f} $ = {valeur_ligne:.2f} $ {tendance} ({variation_pct:+.2f}%)"
            )
            valeur_totale += valeur_ligne
            variation_totale += (cours - prev_close) * quantite
        except Exception as e:
            lignes.append(f"  {symbole} : erreur ({e})")

    result = "=== PORTEFEUILLE ===\n"
    result += '\n'.join(lignes)
    result += f"\n\nValeur totale : {valeur_totale:,.2f} $"
    if valeur_totale > 0:
        var_pct_global = (variation_totale / (valeur_totale - variation_totale)) * 100 if (valeur_totale - variation_totale) != 0 else 0
        tendance = '📈' if variation_totale >= 0 else '📉'
        result += f"\nVariation du jour : {variation_totale:+,.2f} $ ({var_pct_global:+.2f}%) {tendance}"
    return result


if __name__ == "__main__":
    print("=== Test calculer_portefeuille ===")
    print(calculer_portefeuille("AAPL:10|MSFT:5|TSLA:3"))
