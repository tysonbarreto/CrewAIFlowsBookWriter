import asyncio
from typing import List

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel

from src.crews.write_book_chapter_crew.write_book_chapter_crew import WriteBookChapterCrew
from src.crews.outline_book_crew.outline_crew import OutLineCrew
from src.crews.types import Chapter, ChapterOutline

class BookState(BaseModel):
    title:str="The Current State of AI in September 2024 - Trends Across Industries"
    book: List[Chapter] = []
    book_outline: List[ChapterOutline]=[]
    topic:str = "Exploring the latest trends in AI across different industries as of September 2024"
    goal: str = """
        The goal of this book is to provide a comprehensive overview of the current state of artificial intelligence in September 2024.
        It will delve into the latest trends impacting various industries, analyze significant advancements,
        and discuss potential future developments. The book aims to inform readers about cutting-edge AI technologies
        and prepare them for upcoming innovations in the field.
    """


class BookFlow(Flow[BookState]):
    @start()
    def generate_book_online(self):
        print("Kickoff the Book Outline Crew")
        output = OutLineCrew().crew().kickoff(inputs={"topic":self.state.topic, "goal":self.state.goal})
        chapters=output['chapters']
        print("Chapters:", chapters)
        self.state.book_outline = chapters

    @listen(generate_book_online)
    async def write_chapter(self):
        print("Writing Book Chapters")
        tasks=[]

        async def write_single_chapter(chapter_outline):
            output = WriteBookChapterCrew().crew().kickoff(inputs={"goal":self.state.goal,
                                                                 "topic":self.state.topic,
                                                                 "chapter_title":chapter_outline.title,
                                                                 "chapter_description": chapter_outline.description,
                                                                 "book_outline":[chapter_outline.model_dump_json() for chapter_outline in self.state.book_outline]
                                                                 })
            title=output["title"]
            content=output["content"]
            chapter = Chapter(title=title, content=content)
            return chapter
        
        for chapter_outline in self.state.book_outline:
            print(f"Writing Chapter: {chapter_outline.title}")
            print(f"Description: {chapter_outline.description}")
            tasks = asyncio.create_task(write_single_chapter(chapter_outline=chapter_outline))
        
        chapters = await asyncio.gather(*tasks)
        print("Newly generate chapters:", chapters)
        self.state.book.extend(chapters)

        print("Book Chapters", self.state.book)

    @listen(write_chapter)
    async def join_and_save_chapter(self):
        print("Joining and Saving Book Chapters")
        book_content=""

        for chapter in self.state.book:
            book_content += f"# {chapter.title}\n\n"
            book_content += f"{chapter.title}\n\n"
        
        book_title = self.state.title
        filename = f"./{book_title.replace(' ','_')}.md"

        with open(filename,"w", encoding="utf-8") as file:
            file.write(book_content)
        
        print(f"Book saved as {filename}")

def kickoff():
    BookFlow().kickoff()

def plot():
    BookFlow().plot()

if __name__=="__main__":
    kickoff()
