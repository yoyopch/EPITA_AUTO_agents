# A3 — Outil de recherche web via TavilySearch.
# Permet à l'agent de chercher des informations sur internet (actualités, infos entreprises, etc.)

import os
from langchain_community.tools import TavilySearchResults


def creer_outil_recherche_web():
    """Crée et retourne l'outil TavilySearchResults configuré."""
    return TavilySearchResults(
        max_results=3,
        tavily_api_key=os.getenv("TAVILY_API_KEY")
    )


def rechercher_web(query: str) -> str:
    """
    Recherche des informations sur le web via Tavily.
    Entrée : requête de recherche en texte libre.
    Exemple : "dernières actualités Apple 2024"
    """
    try:
        outil = creer_outil_recherche_web()
        resultats = outil.invoke(query)
        if not resultats:
            return "Aucun résultat trouvé."
        reponse = "Résultats de recherche web :\n"
        for i, r in enumerate(resultats, 1):
            titre = r.get("url", "Sans titre")
            contenu = r.get("content", "Pas de contenu")[:200]
            reponse += f"\n{i}. {titre}\n   {contenu}\n"
        return reponse
    except Exception as e:
        return f"Erreur lors de la recherche web : {e}"


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    print("=== Test rechercher_web ===")
    print(rechercher_web("cours action Apple 2024"))
