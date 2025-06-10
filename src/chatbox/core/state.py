from typing import List, TypedDict, Literal, Annotated, Optional
from pydantic import BaseModel, Field
import operator

class SectionInput(BaseModel):
    query: str = Field(description="user's query")

class SectionOutput(BaseModel):
    conclusion: str = Field(description="conclusion")

class SectionState(TypedDict):
    query: str
    conclusion: str