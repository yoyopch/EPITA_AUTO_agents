# D1 — API REST pour interroger l'agent LangChain via HTTP.
# Lancer avec : uvicorn api:app --reload
# Endpoint : POST /api/agent/query  {"question": "..."}

import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel

from agent import creer_agent
from tools.portfolio_db import consulter_portfolio, identifier_actifs_risques
from langchain_classic.tools import Tool

app = FastAPI(
    title="Agent LangChain API",
    description="API REST pour interroger l'agent LangChain avec outils financiers et portfolio.",
    version="1.0.0"
)

# Outils supplémentaires pour le portfolio (D1)
from agent import tools as base_tools

portfolio_tools = [
    Tool(name='consulter_portfolio', func=consulter_portfolio,
         description='Consulte le portefeuille financier stocké en base PostgreSQL. '
                     'Retourne positions, cours actuels, PnL. '
                     'Entrée : nom d\'utilisateur (optionnel, défaut: demo).'),
    Tool(name='actifs_risques', func=identifier_actifs_risques,
         description='Identifie les actifs les plus risqués du portefeuille (en perte). '
                     'Entrée : nom d\'utilisateur (optionnel, défaut: demo).'),
]

# Création de l'agent enrichi avec les outils portfolio
all_tools = base_tools + portfolio_tools


def creer_agent_api():
    """Crée un agent avec tous les outils (base + portfolio)."""
    from langchain_openai import ChatOpenAI
    from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_classic.memory import ConversationBufferMemory

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Tu es un agent d'analyse de portefeuille financier. Tu disposes d'outils "
         "pour consulter des clients, produits, cours boursiers, portefeuilles en base "
         "PostgreSQL, et effectuer des calculs financiers."),
        MessagesPlaceholder("chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])
    agent = create_openai_tools_agent(llm=llm, tools=all_tools, prompt=prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=all_tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True,
        memory=memory,
        return_intermediate_steps=True
    )
    return agent_executor


agent_instance = None


def get_agent():
    global agent_instance
    if agent_instance is None:
        agent_instance = creer_agent_api()
    return agent_instance


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    response: str
    tools_used: list[str]


@app.post("/api/agent/query", response_model=QuestionResponse)
def query_agent(req: QuestionRequest):
    """Envoie une question à l'agent et retourne la réponse avec les outils utilisés."""
    agent = get_agent()
    result = agent.invoke({"input": req.question})
    tools_used = []
    if "intermediate_steps" in result:
        for step in result["intermediate_steps"]:
            if hasattr(step[0], "tool"):
                tools_used.append(step[0].tool)
    return QuestionResponse(
        response=result["output"],
        tools_used=tools_used
    )


@app.get("/api/health")
def health():
    """Endpoint de vérification que l'API est en ligne."""
    return {"status": "ok"}


@app.get("/api/tools")
def list_tools():
    """Liste tous les outils disponibles pour l'agent."""
    return [{"name": t.name, "description": t.description} for t in all_tools]
