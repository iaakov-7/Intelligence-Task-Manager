from fastapi import FastAPI,HTTPException
import mysql.connector
from contextlib import asynccontextmanager
from database.db_connection import db
from routes.agent_routes import router as agent_touter
from routes.mission_routes import router as mission_touter
from routes.report_routes import router as report_touter


@asynccontextmanager
async def lifespan(app:FastAPI):
    db.create_database()
    db.create_tables()
    yield
    db.close_connection()

           

app = FastAPI(lifespan=lifespan)

app.include_router(agent_touter,prefix="/agents")
app.include_router(mission_touter,prefix="/missions")
app.include_router(report_touter,prefix="/reports")