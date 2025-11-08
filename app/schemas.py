from pydantic import BaseModel
from typing import Optional


class QueryRequest(BaseModel):
    query: str


class IntentAndContainer(BaseModel):
    intent: str
    container: str