from pydantic import BaseModel
from typing import List

class ChapterOutline(BaseModel):
    title:str
    description:str

class BookOutLine(BaseModel):
    chapters:List[ChapterOutline]

class Chapter(BaseModel):
    title:str
    content:str


if __name__=="__main__":
    __all__=["ChapterOutline","BookOutLine","Chapter"]

