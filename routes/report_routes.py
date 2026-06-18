from fastapi import APIRouter, HTTPException
import mysql.connector
from database.agent_db import db_agent
from database.mission_db import db_mission
from logs.logger_config import logger

router = APIRouter(tags=["Reports"])

@router.get("/summary")
def get_general_report():
    logger.info("Incoming request: get general report")
    general = { 
  "active_agents_count": db_agent.count_active_agents().get("active_agents"), 
  "total_missions": db_mission.count_all_missions().get("total_missions"),
  "open_missions": db_mission.count_open_missions().get("total_open_missions"),
  "completed_missions": db_mission.count_by_status("COMPLETED").get("total"), 
  "failed_missions": db_mission.count_by_status("FAILED").get("total"), 
  "critical_missions": db_mission.count_critical_missions().get("total_critical_missions")
    }
    logger.info("Readed general report")
    return general

@router.get("/missions-by-status")
def get_by_status():
    logger.info("Incoming request: get report by status")
    report = { 
  "open": db_mission.count_open_missions().get("total_open_missions"), 
  "in_progress": db_mission.count_by_status("IN_PROGRESS").get("total"), 
  "completed":db_mission.count_by_status("COMPLETED").get("total"), 
  "failed": db_mission.count_by_status("FAILED").get("total"),
   "cancelled":db_mission.count_by_status("CANCELLED").get("total") }
    logger.info("Readed report by status")
    return report

@router.get("/top-agent")
def get_top_agent():
    logger.info("Incoming request: get top agent report")
    if len(db_agent.get_all_agents()) == 0:
        logger.error("There are no agents in db")
        raise HTTPException(404,"There are no agents in db")
    top = db_mission.get_top_agent()
    logger.info("Readed top agent report")
    return top