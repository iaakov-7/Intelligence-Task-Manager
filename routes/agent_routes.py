from fastapi import APIRouter, HTTPException
from database.agent_db import db_agent
from utils.models import Agent, AgentUpdate, check_int

router = APIRouter(tags=["Agents"])


@router.post("",status_code=201)
def create_agent(new_agent:Agent):
    dict_agent = new_agent.model_dump()
    if dict_agent["agent_rank"] not in['Junior', 'Senior', 'Commander']:
        raise HTTPException(400,"Not legal runk") 
    db_agent.create_agent(dict_agent)
    return {"Message":"Agent created"}

@router.get("")
def get_agents():
    agents = db_agent.get_all_agents()
    return agents

@router.get("/{id}")
def get_by_id(id:int):
    check_int(id)
    agent = db_agent.get_agent_by_id(id)
    if not agent:
        raise HTTPException(404,f"Agent {id} not found")
    return agent

@router.put("/{id}")
def update_agent(id:int,to_update:AgentUpdate):
    check_int(id)
    if not db_agent.get_agent_by_id(id):
         raise HTTPException(404,f"Agent {id} not found")
    agent_dict = to_update.model_dump(exclude_unset=True)
    updated = db_agent.update_agent(id,agent_dict)
    return {"Message":updated}

@router.put("/{id}/deactivate")
def deactivate(id:int):
    check_int(id)
    if not db_agent.get_agent_by_id(id):
         raise HTTPException(404,f"Agent {id} not found")    
    updated = db_agent.deactivate_agent(id)
    return {"Message":updated}

@router.get("{id}/performance")
def get_performance(id:int):
    check_int(id)
    if not db_agent.get_agent_by_id(id):
         raise HTTPException(404,f"Agent {id} not found") 
    result = db_agent.get_agent_performance(id)
    return result       
