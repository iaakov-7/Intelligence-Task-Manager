from pydantic import BaseModel
from fastapi import HTTPException

class Agent(BaseModel):
    name:str 
    specialty:str 
    agent_rank:str

class AgentUpdate(BaseModel):
    name:str | None = None
    specialty:str | None = None
    agent_rank:str| None = None   


def check_int(id):
    if not isinstance(id,int):
        raise HTTPException(422,"Id most be integer")

