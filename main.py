import os
from dotenv import load_dotenv
from agent import creer_agent, interroger_agent

load_dotenv()

SCENARIOS = {
    "1": (
        "Scénario 1 – Consultation base de données",
        "Quelles sont les informations du client Marie Dupont ? "
        "Quel est son solde et son type de compte ?"
    ),
    "2": (
        "Scénario 2 – Données financières",
        "Donne-moi le cours actuel d'Apple (AAPL) et du Bitcoin (BTC). "
        "Lequel a la plus forte variation aujourd'hui ?"
    ),
    "3": (
        "Scénario 3 – Calculs financiers multiples",
        "Je veux acheter un ordinateur portable (P001). "
        "Quel est son prix TTC avec la TVA à 20% ? "
        "Et quelle serait ma marge si je le revendais 1200€ ?"
    ),
    "4": (
        "Scénario 4 – Conversion de devises (API)",
        "Combien vaut 500 euros en dollars américains et en livres sterling ? "
        "Donne-moi les deux conversions."
    ),
    "5": (
        "Scénario 5 – Calcul de prêt + intérêts",
        "Je souhaite emprunter 150 000€ sur 20 ans à un taux de 4% par an. "
        "Quelle serait ma mensualité et combien paierais-je d'intérêts au total ? "
        "Si je place 20 000€ à 3% pendant 5 ans, quel capital j'obtiendrai-je ?"
    ),
    "6": (
        "Scénario 6 – Recommandation personnalisée",
        "Je suis un client Premium avec un budget de 400€. "
        "Je cherche du matériel informatique. "
        "Quels produits me recommanderais-tu ?"
    ),
    "7": (
        "Scénario 7 – Analyse de texte complète",
        "Résume ce texte : 'LangChain est un framework pour construire des "
        "applications intelligentes basées sur des modèles de langage.' "
        "Extrait ensuite les mots-clés et formate un rapport avec "
        "les champs Sujet:LangChain|Type:Résumé|Auteur:Agent."
    ),
    "8": (
        "Scénario 8 – Analyse financière complète (multi-outils)",
        "Analyse financière : "
        "1) Cours de Microsoft (MSFT) et d'Ethereum (ETH). "
        "2) Convertis 1000 USD en EUR. "
        "3) Si j'investis 5000€ à 7% pendant 10 ans, quel capital ?"
    ),
}

# C2 — Scénario 9 : Démonstration de la mémoire conversationnelle (3 questions enchaînées)
SCENARIO_MEMOIRE = [
    "Quelles sont les informations de Sophie Bernard ?",
    "En fonction de son type de compte et d'un budget de 500€ en informatique, que lui recommandes-tu ?",
    "Quel est le prix TTC du premier produit recommandé ? A-t-elle assez sur son solde ?",
]


def afficher_menu():
    print("\n" + "="*60)
    print("        AGENT LANGCHAIN — MENU DES SCÉNARIOS")
    print("="*60)
    for num, (titre, _) in SCENARIOS.items():
        print(f"  {num}. {titre}")
    print("  9. Scénario 9 – Mémoire conversationnelle (C2)")
    print("  quit — Quitter")
    print("="*60)


if __name__ == "__main__":
    print("Initialisation de l'agent...")
    agent = creer_agent()
    print("Agent prêt.")

    while True:
        afficher_menu()
        choix = input("\nVotre choix : ").strip().lower()

        if choix in ("quit", "exit", "q"):
            print("\nAu revoir !")
            break
        elif choix == "9":
            # C2 — Scénario mémoire conversationnelle : 3 questions enchaînées
            print("\n>>> Scénario 9 – Mémoire conversationnelle (C2)")
            print("L'agent doit retenir le contexte entre les 3 questions.\n")
            for i, question in enumerate(SCENARIO_MEMOIRE, 1):
                print(f"\n--- Question {i}/3 ---")
                interroger_agent(agent, question)
        elif choix in SCENARIOS:
            titre, question = SCENARIOS[choix]
            print(f"\n>>> {titre}")
            interroger_agent(agent, question)
        else:
            print(f"\n  Choix invalide '{choix}'. Entrez un numéro entre 1 et 9, ou 'quit'.")


