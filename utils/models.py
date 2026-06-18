from pydantic import BaseModel


class Agent(BaseModel):
    name:str 
    specialty:str 
    agent_rank:str

class AgentUpdate(BaseModel):
    name:str | None = None
    specialty:str | None = None
    agent_rank:str| None = None   