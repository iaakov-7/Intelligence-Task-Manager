from database.db_connection import db
from database.agent_db import db_agent
from database.db_exceptions import AgentNotActiveError,AgentCannotHaveThreeOpentasksError,MissionOnlyForCommanderError,MissionStatusError

class MissionDB:
    def __init__(self):
        self.db = db
        self.db_agent = db_agent

    def create_mission(self, data:int):   
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """INSERT INTO missions(title,description,location,difficulty,importance,risk_level)
                    VALUES(%s,%s,%s,%s,%s,%s)"""
        values = [data.get('title'),data.get('description'),data.get('location'),data.get('difficulty'),data.get('importance')]
        risk_level_num = data.get('difficulty') * 2 + data.get('importance')
        if risk_level_num <= 9:
            risk_level = "LOW"
        elif risk_level_num <= 17:
            risk_level = "MEDIUM" 
        elif risk_level_num <= 24:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"           
        cursor.execute(query,values+[risk_level])
        conn.commit()
        id = cursor.lastrowid
        cursor.execute("SELECT * FROM missions WHERE id = %s",(id,))
        new_mission = cursor.fetchone()
        cursor.close() 
        return new_mission 
    
    def get_all_missions(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions")
        missions = cursor.fetchall()
        cursor.close()
        return missions
    
    def get_mission_by_id(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions WHERE id= %s",(id,))
        mission = cursor.fetchone()
        cursor.close()
        return mission
    
    def assign_mission(self,m_id:int, a_id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True) 
        agent = db_agent.get_agent_by_id(a_id)
        mission = self.get_mission_by_id(m_id)
        if agent["is_active"] == False:
            raise AgentNotActiveError
        if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != 'Commander':
                raise MissionOnlyForCommanderError
        if mission["status"].lower() != "new":
             raise MissionStatusError
        cursor.execute("""SELECT * FROM missions WHERE assigned_agent_id=%s""",(a_id,))
        agent_missions = cursor.fetchall()
        count_open_missions = 0
        for a_mission in agent_missions:
            if a_mission["status"].lower() in ["assigned","in_progress"]:
                count_open_missions += 1
        if count_open_missions >= 3:
                raise AgentCannotHaveThreeOpentasksError
        cursor.execute("UPDATE missions SET status='ASSIGNED',assigned_agent_id=%s WHERE id=%s",(a_id,m_id))
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        if updated:
            return f"Mission {m_id} assigned to agent {a_id}"
        return "Assign failed"
    
    def update_mission_status(self,id:int, status:str):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        mission = self.get_mission_by_id(id)
        status_mission = mission["status"]
        if status == "IN_PROGRESS":
            if status_mission != "ASSIGNED":
                raise MissionStatusError
        elif status == "COMPLETED" or status == "FAILED":
            if status_mission != "IN_PROGRESS":
                raise MissionStatusError
        elif status == "CANCELLED": 
            if status_mission != "NEW" and status_mission != "ASSIGNED":
                raise MissionStatusError
        cursor.execute("UPDATE missions SET status=%s WHERE id=%s",(status,id))  
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        if updated:
             return f"Status updated successfully"
        return "Update failed"

    def get_open_missions_by_agent(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM missions WHERE assigned_agent_id=%s AND (status='ASSIGNED' OR status='IN_PROGRESS')",(id,)) 
        open_missions = cursor.fetchall()
        cursor.close()
        return open_missions  

    def count_all_missions(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT COUNT(*) AS total_missions FROM missions""") 
        count_missions = cursor.fetchone()
        cursor.close()
        return count_missions
    
    def count_by_status(self,status):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)        	
        cursor.execute("""SELECT status, COUNT(*) AS total FROM missions WHERE status=%s""",(status,))
        count = cursor.fetchone()
        cursor.close()
        return count 

    def count_open_missions(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)        	
        cursor.execute("""SELECT COUNT(*) AS total_open_missions FROM missions WHERE status="IN_PROGRESS" OR status="ASSIGNED" """)
        count = cursor.fetchone()
        cursor.close()
        return count  

    def count_critical_missions(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)        	
        cursor.execute("SELECT  COUNT(*) AS total_critical_missions FROM missions WHERE risk_level='CRITICAL'")
        count = cursor.fetchone()
        cursor.close()
        return count 

    def get_top_agent(self):              
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)        	
        cursor.execute("SELECT * FROM agents ORDER BY completed_missions DESC LIMIT 1")
        count = cursor.fetchone()
        cursor.close()
        return count 

db_mission = MissionDB()





