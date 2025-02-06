from crewai import Agent, Task, Crew, Process
from crewai.project import crew, agent, task, CrewBase
from crewai_tools import SerperDevTool
from langchain_openai import ChatOpenAI

from src.crews.types import Chapter

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@CrewBase
class WriteBookChapterCrew:
    """Write Book Chapter Crew"""

    agents_config="config/agents.yml"
    tasks_config="config/tasks.yml"
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
    def writer(self)->Agent:
        return Agent(
            config=self.agents_config['writer'],
            llm=self.llm,
            verbose=True
        )
    
    @task
    def research_chapter(self)->Task:
        return Task(
            config=self.tasks_config['research_chapter']
        )

    @task
    def write_chapter(self)->Task:
        return Task(
            config=self.tasks_config['write_chapter'],
            output_pydantic=Chapter
        )
    
    @crew
    def crew(self):
        """Creates the Write Book Chapter Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
    

if __name__=="__main__":
    __all__=["WriteBookChapterCrew"]