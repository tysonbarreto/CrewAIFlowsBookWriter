from crewai.project import crew, agent, task, CrewBase
from crewai import Crew, Agent, Task, Process
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI

from src.crews.types import BookOutLine

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@CrewBase
class OutLineCrew:
    """
    Book Outline Crew

    """
    agents_config = "config/agents.yml"
    tasks_config = "config/tasks.yml"
    llm=ChatOpenAI(model="gpt-4o-mini")

    @agent
    def researcher(self)->Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[SerperDevTool()],
            llm=self.llm,
            verbose=True
        )
    
    @agent
    def outliner(self)->Agent:
        return Agent(
            config=self.agents_config['outliner'],
            tools=[SerperDevTool()],
            llm=self.llm,
            verbose=True
        )
    
    @task
    def research_topic(self)->Task:
        return Task(
            config=self.tasks_config['research_topic']
        )
    
    @task
    def generate_outline(self)->Task:
        return Task(
            config=self.tasks_config['generate_outline'],
            output_pydantic=BookOutLine
        )

    @crew
    def crew(self)->Crew:
        """Creates the Book Outline Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
    
if __name__=="__main__":
    __all__=["OutLineCrew"]
