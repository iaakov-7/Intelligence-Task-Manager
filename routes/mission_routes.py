from fastapi import APIRouter,HTTPException
from database.mission_db import db_mission
from database.agent_db import db_agent
import database.db_exceptions
from utils.models import Mission, check_int

router = APIRouter(tags=["Missions"])


@router.post("",status_code=201)
def create_mission(new_mission:Mission):
    dict_mission = new_mission.model_dump()
    if dict_mission['difficulty'] not in range(1,11):
        raise HTTPException(400,"Difficulty must be between 1-10")
    if dict_mission['importance'] not in range(1,11):
        raise HTTPException(400,"Importance must be between 1-10")
    db_mission.create_mission(dict_mission)
    return {"Message":"Mission created successfully"}

@router.get("")
def get_missions():
    missions = db_mission.get_all_missions()
    return missions

@router.get("/{id}")
def get_mission_by_id(id:int):
    check_int(id)
    mission = db_mission.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404,f"Mission {id} not found")
    return mission

@router.put("/{id}/assign/{agent_id}")
def assign_mission(id:int,agent_id:int):
    check_int(id)
    check_int(agent_id)
    if not db_mission.get_mission_by_id(id):
        raise HTTPException(404,f"Mission {id} not found")
    if not db_agent.get_agent_by_id(agent_id):
        raise HTTPException(404,f"Agent {agent_id} not found")
    try:
        assigned = db_mission.assign_mission(id,agent_id)
    except database.db_exceptions.MissionStatusError:
        raise HTTPException(400,"Mission not available")    
    except database.db_exceptions.AgentNotActiveError:
        raise HTTPException(400,"Agent is not active")
    except database.db_exceptions.AgentCannotHaveThreeOpentasksError:
        raise HTTPException(400,"Agent has reached maximum missions")
    except database.db_exceptions.MissionOnlyForCommanderError:
        raise HTTPException(400,"Only Commander can handle critical missions")
    return {"Message":assigned}

@router.put("/{id}/start")
def start_mission(id:int,status:str | None = None):
    check_int(id)
    if not db_mission.get_mission_by_id(id):
        raise HTTPException(404,f"Mission {id} not found")
    if status is None:
        status = "IN_PROGRESS"
    if status.upper() != "IN_PROGRESS":
        raise HTTPException(400,"Status must be IN_PROGRESS")
    try:
        updated = db_mission.update_mission_status(id,status.upper())
    except database.db_exceptions.MissionStatusError:
        raise HTTPException(400,"Mission must be ASSIGNED before starting")    
    return {"Message":updated}

@router.put("/{id}/complete")
def complete_mission(id:int,status:str| None = None):
    check_int(id)
    mission = db_mission.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404,f"Mission {id} not found")
    if status is None:
        status = "COMPLETED"
    if status.upper() != "COMPLETED":
        raise HTTPException(400,"Status must be COMPLETED")
    try:
        updated = db_mission.update_mission_status(id,status.upper())
    except database.db_exceptions.MissionStatusError:
        raise HTTPException(400,"Mission must be IN_PROGRESS before completed")
    db_agent.increment_completed(mission["assigned_agent_id"])   
    return {"Message":updated}

@router.put("/{id}/fail")
def fail_mission(id:int,status:str | None = None):
    check_int(id)
    mission = db_mission.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404,f"Mission {id} not found")
    if status is None:
        status = "FAILED"
    if status.upper() != "FAILED":
        raise HTTPException(400,"Status must be FAILED")
    try:
        updated = db_mission.update_mission_status(id,status.upper())
    except database.db_exceptions.MissionStatusError:
        raise HTTPException(400,"Mission must be IN_PROGRESS before failed")
    db_agent.increment_failed(mission["assigned_agent_id"])   
    return {"Message":updated}

@router.put("/{id}/cancel")
def cancel_mission(id:int,status:str| None = None):
    check_int(id)
    mission = db_mission.get_mission_by_id(id)
    if not mission:
        raise HTTPException(404,f"Mission {id} not found")
    if status is None:
        status = "CANCELLED"
    if status.upper() != "CANCELLED":
        raise HTTPException(400,"Status must be CANCELLED")
    try:
        updated = db_mission.update_mission_status(id,status.upper())
    except database.db_exceptions.MissionStatusError:
        raise HTTPException(400,"Mission must be ASSIGNED or NEW before cancelled") 
    return {"Message":updated}