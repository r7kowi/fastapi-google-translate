
from pydantic import BaseModel, Field
from typing import List

class WordParams(BaseModel):
    original_language: str = Field(..., example="en") 
    translated_language: str = Field(..., example="es")
    primary_translation: str = Field(..., example="hola")
    alternative_translations: List[str] = Field(None, example=["hey", "hi"], nullable=True)
    synonyms: List[str] = Field(None, example=["greetings", "salutations"], nullable=True)
    primary_definition: str = Field(None, example="used as a greeting or to begin a telephone conversation", nullable=True)
    example_use: str = Field(None, example="hello there, Katie!", nullable=True)


class WordResponse(BaseModel):
    status: int = Field(..., example=200)
    word: str = Field(..., example="hello")
    attributes: WordParams

class Wordlist(BaseModel):
    wordlist: List[str] = Field(..., example=["hello", "goodbye", "good morning", "good night"]) 

class WordDetailed(BaseModel):
    word: str = Field(..., example="hello")
    attributes: WordParams 

class DeleteResponse(BaseModel):
    status: int = Field(..., example=200)
    message: str = Field(..., example="Word deleted successfully")