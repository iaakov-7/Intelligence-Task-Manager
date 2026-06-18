from fastapi import APIRouter, HTTPException
from database.agent_db import db_agent
from utils.models import Agent, AgentUpdate

router = APIRouter(tags=["Agents"])


@router.post("",status_code=201)
def create_agent(new_agent:Agent):
    dict_agent = new_agent.model_dump()
    if dict_agent["agent_rank"] not in['Junior', 'Senior', 'Commander']:
        raise HTTPException(400,) 
    db_agent.create_agent(dict_agent)
    