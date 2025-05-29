import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from .tools.send_email_tool import SendEmailTool
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage

from chromadb import EmbeddingFunction

class MyCohereEmbedder(EmbeddingFunction):
    def __init__(self, api_key, model):
        import cohere
        self.client = cohere.Client(api_key)
        self.model = model

    def __call__(self, texts):
        response = self.client.embed(
            texts=texts,
            model=self.model,
            input_type="search_document",
            embedding_types=["float"]
        )
        # Aquí extraes solo los embeddings
        return response.embeddings  # O response["embeddings"] según SDK


class TrendingCompany(BaseModel):
    """ Una empresa que está en las noticias y atrayendo atención """
    name: str = Field(description="Nombre de la empresa")
    ticker: str = Field(description="Símbolo bursátil")
    reason: str = Field(description="Razón por la que esta empresa está en tendencia en las noticias")

class TrendingCompanyList(BaseModel):
    """ Lista de múltiples empresas en tendencia que aparecen en las noticias """
    companies: List[TrendingCompany] = Field(description="Lista de empresas en tendencia en las noticias")

class TrendingCompanyResearch(BaseModel):
    """ Investigación detallada sobre una empresa """
    name: str = Field(description="Nombre de la empresa")
    market_position: str = Field(description="Posición actual en el mercado y análisis competitivo")
    future_outlook: str = Field(description="Perspectivas futuras y de crecimiento")
    investment_potential: str = Field(description="Potencial de inversión y idoneidad para invertir")

class TrendingCompanyResearchList(BaseModel):
    """ Lista de investigaciones detalladas de todas las empresas """
    research_list: List[TrendingCompanyResearch] = Field(description="Investigación exhaustiva de todas las empresas en tendencia")

@CrewBase
class StockPicker():
    """Equipo StockPicker"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(config=self.agents_config['trending_company_finder'],
                     tools=[SerperDevTool()], memory=True)
    
    @agent
    def financial_researcher(self) -> Agent:
        return Agent(config=self.agents_config['financial_researcher'], 
                     tools=[SerperDevTool()]) # no queremos memoria aquí ya que queremos que siempre busque en Internet
    @agent
    def stock_picker(self) -> Agent:
        return Agent(config=self.agents_config['stock_picker'], 
                     tools=[SendEmailTool()], memory=True)

    @task
    def find_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['find_trending_companies'],
            output_pydantic=TrendingCompanyList,
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config['research_trending_companies'],
            output_pydantic=TrendingCompanyResearchList,
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config['pick_best_company'],
        )

    @crew
    def crew(self) -> Crew:
        """Crea el equipo StockPicker"""

        manager = Agent(
            config=self.agents_config['manager'],
            allow_delegation=True
        )
            
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True,
            # Memoria a largo plazo para almacenamiento persistente entre sesiones
            long_term_memory = LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./memory/long_term_memory_storage.db"
                )
            ),
            # Memoria a corto plazo para contexto actual usando RAG
            short_term_memory = ShortTermMemory(
                storage = RAGStorage(
                        # El formato de Cohere no se adapta a lo que espera CrewAI y se ha creado una clase adaptadora
                        embedder_config = {
                            "provider": "custom",
                            "config": {
                                "embedder": MyCohereEmbedder(os.environ.get("COHERE_API_KEY"), 'embed-multilingual-v3.0')
                            }
                        },
                        # embedder_config={
                        #     "provider": "cohere",
                        #     "config": {
                        #         "api_key": os.environ.get("COHERE_API_KEY"),
                        #         "model": 'embed-multilingual-v3.0'
                        #     }
                        # },
                        type="short_term",
                        path="./memory/"
                    )
                ),
            # Memoria de entidades para rastrear información clave sobre entidades
            entity_memory = EntityMemory(
                storage=RAGStorage(
                    embedder_config = {
                            "provider": "custom",
                            "config": {
                                "embedder": MyCohereEmbedder(os.environ.get("COHERE_API_KEY"), 'embed-multilingual-v3.0')
                            }
                    },
                    # embedder_config={
                    #     "provider": "cohere",
                    #     "config": {
                    #         "api_key": os.environ.get("COHERE_API_KEY"),
                    #         "model": 'embed-multilingual-v3.0'
                    #     }
                    # },
                    type="short_term",
                    path="./memory/"
                )
            ),
        )
