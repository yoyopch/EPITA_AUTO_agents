from langchain_classic.tools import Tool

from tools.database import rechercher_client, rechercher_produit
from tools.finance import obtenir_cours_action, obtenir_cours_crypto
from tools.calculs import calculer_interets_composes, calculer_marge, calculer_mensualite_pret, calculer_tva
from tools.api_publique import convertir_devise
from tools.texte import  extraire_mots_cles, formater_rapport, resumer_texte
from tools.recommandation import recommander_produits
# A3 — Recherche web
from tools.recherche_web import rechercher_web
# B1 — Portefeuille boursier
from tools.portefeuille import calculer_portefeuille
# B2 — Exécution de code Python
# ATTENTION : PythonREPLTool exécute du code arbitraire. À utiliser avec précaution.
from langchain_experimental.tools import PythonREPLTool

python_repl = PythonREPLTool()
python_repl.description = (
    'Exécute du code Python pour des calculs complexes ou traitements '
    'de données non couverts par les autres outils. '
    'Entrée : code Python valide sous forme de chaîne.'
)
# ATTENTION SECURITE : cet outil exécute du code arbitraire.
# Ne jamais utiliser en production sans sandbox.

tools =[
    # ── Outil 1 : Base de données ─────────────────────────────────────
    Tool(name='rechercher_client', func=rechercher_client,
         description='Recherche un client par nom ou ID (ex: C001). '
                     'Retourne solde, type de compte, historique achats.'),
    Tool(name='rechercher_produit', func=rechercher_produit,
         description='Recherche un produit par nom ou ID. '
                     'Retourne prix HT, TVA, prix TTC, stock.'),
    # ── Outil 2 : Données financières ─────────────────────────────────
    Tool(name='cours_action', func=obtenir_cours_action,
         description='Cours boursier d\'une action. '
                     'Entrée : symbole majuscule ex AAPL, MSFT, TSLA, LVMH, AIR.'),
    Tool(name='cours_crypto', func=obtenir_cours_crypto,
         description='Cours d\'une crypto. '
                     'Entrée : symbole ex BTC, ETH, SOL, BNB, DOGE.'),
    # ── Outil 3 : Calculs financiers ──────────────────────────────────
    Tool(name='calculer_tva', func=calculer_tva,
         description='Calcule TVA et prix TTC. Entrée : prix_ht,taux ex 100,20.'),
    Tool(name='calculer_interets', func=calculer_interets_composes,
         description='Intérêts composés. Entrée : capital,taux_annuel,années ex 10000,5,3.'),
    Tool(name='calculer_marge', func=calculer_marge,
         description='Marge commerciale. Entrée : prix_vente,cout_achat ex 150,80.'),
    Tool(name='calculer_mensualite', func=calculer_mensualite_pret,
         description='Mensualité prêt. Entrée : capital,taux_annuel,mois ex 200000,3.5,240.'),
    # ── Outil 4 : API publique ────────────────────────────────────────
    Tool(name='convertir_devise', func=convertir_devise,
         description='Conversion de devises en temps réel (API Frankfurter). '
                     'Entrée : montant,DEV_SOURCE,DEV_CIBLE ex 100,USD,EUR.'),
    # ── Outil 5 : Transformation de texte ────────────────────────────
    Tool(name='resumer_texte', func=resumer_texte,
         description='Résume un texte et donne des statistiques. Entrée : texte complet.'),
    Tool(name='formater_rapport', func=formater_rapport,
         description='Formate en rapport. Entrée : Cle1:Val1|Cle2:Val2.'),
    Tool(name='extraire_mots_cles', func=extraire_mots_cles,
         description='Extrait les mots-clés d\'un texte. Entrée : texte complet.'),
    # ── Outil 6 : Recommandation ─────────────────────────────────────
    Tool(name='recommander_produits', func=recommander_produits,
         description='Recommandations produits. '
                     'Entrée : budget,categorie,type_compte ex 300,Informatique,Premium. '
                     'Catégories : Informatique, Mobilier, Audio, Toutes. '
                     'Types : Standard, Premium, VIP.'),
    # ── Outil 7 : Recherche web (A3) ────────────────────────────────
    Tool(name='recherche_web', func=rechercher_web,
         description='Recherche des informations sur internet (actualités, entreprises, etc.). '
                     'Entrée : requête de recherche en texte libre.'),
    # ── Outil 8 : Portefeuille boursier (B1) ────────────────────────
    Tool(name='calculer_portefeuille', func=calculer_portefeuille,
         description='Calcule la valeur d\'un portefeuille boursier. '
                     'Entrée : SYMBOLE1:QUANTITE1|SYMBOLE2:QUANTITE2 ex AAPL:10|MSFT:5|TSLA:3.'),
    # ── Outil 9 : Exécution Python (B2) ─────────────────────────────
    # ATTENTION SECURITE : Cet outil exécute du code Python arbitraire.
    # Ne jamais utiliser en production sans sandbox.
    Tool(name='python_repl', func=python_repl.run,
         description=python_repl.description),
]

def creer_agent():
    """Crée et retourne un agent LangChain configuré avec mémoire conversationnelle."""
    from langchain_openai import ChatOpenAI
    from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_classic.memory import ConversationBufferMemory
    import os

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0, 
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Tu es un assistant financier intelligent. Tu disposes de plusieurs outils "
         "pour aider les utilisateurs avec leurs questions sur les clients, produits, "
         "cours boursiers, calculs financiers, recommandations et recherches web."),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True,
        memory=memory
    )
    return agent_executor


def interroger_agent(agent, question: str):
    """Envoie une question à l'agent et affiche la réponse finale."""
    print(f"\n{'='*60}")
    print(f"Question : {question}")
    print('='*60)
    result = agent.invoke({"input": question})
    print(f"\nRéponse finale : {result['output']}")
    return result
