from fastapi import APIRouter, HTTPException
from database.agent_db import db_agent
from utils.models import Agent, AgentUpdate, check_int
from logs.logger_config import logger

router = APIRouter(tags=["Agents"])


@router.post("",status_code=201)
def create_agent(new_agent:Agent):
    logger.info("Incoming request: create agent")
    dict_agent = new_agent.model_dump()
    if dict_agent["agent_rank"] not in['Junior', 'Senior', 'Commander']:
        logger.error("Not legal runk")
        raise HTTPException(400,"Not legal runk") 
    db_agent.create_agent(dict_agent)
    logger.info("Created agent successfully")
    return {"Message":"Agent created"}

@router.get("")
def get_agents():
    logger.info("Incoming request: get agents")
    agents = db_agent.get_all_agents()
    if len(agents) == 0:
        logger.warning("There are no agents")
    logger.info("Readed all agents successfully")    
    return agents

@router.get("/{id}")
def get_by_id(id:int):
    logger.info("Incoming request: get agent %s",id)
    check_int(id)
    agent = db_agent.get_agent_by_id(id)
    if not agent:
        logger.error("Agent %s not found",id)
        raise HTTPException(404,f"Agent {id} not found")
    logger.info("Readed agent %s successfully",id)
    return agent

@router.put("/{id}")
def update_agent(id:int,to_update:AgentUpdate):
    logger.info("Incoming request: update agent %s",id)
    check_int(id)
    if not db_agent.get_agent_by_id(id):
         logger.error("Agent %s not found",id)
         raise HTTPException(404,f"Agent {id} not found")
    agent_dict = to_update.model_dump(exclude_unset=True)
    updated = db_agent.update_agent(id,agent_dict)
    logger.info("Updated agent %s successfully",id)
    return {"Message":updated}

@router.put("/{id}/deactivate")
def deactivate(id:int):
    logger.info("Incoming request: deactivate agent %s",id)
    check_int(id)
    if not db_agent.get_agent_by_id(id):
         logger.error("Agent %s not found",id)
         raise HTTPException(404,f"Agent {id} not found")    
    updated = db_agent.deactivate_agent(id)
    logger.info("Deactivated agent %s successfully",id)
    return {"Message":updated}

@router.get("{id}/performance")
def get_performance(id:int):
    logger.info("Incoming request: get performance agent %s",id)
    check_int(id)
    if not db_agent.get_agent_by_id(id):
         logger.error("Agent %s not found",id)
         raise HTTPException(404,f"Agent {id} not found") 
    result = db_agent.get_agent_performance(id)
    logger.info("Readed performance agent %s successfully",id)
    return result       
