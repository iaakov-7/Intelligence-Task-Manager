from database.db_connection import db
from database.db_exceptions import IdCannotChengedError

class AgentDB:
    def __init__(self):
        self.db = db

    def create_agent(self,data:dict):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """INSERT INTO agents(name, specialty, agent_rank)
                    VALUES(%s,%s,%s)"""
        values = [data.get('name'),data.get('specialty'),data.get('agent_rank')]
        cursor.execute(query,values)
        conn.commit()
        id = cursor.lastrowid
        cursor.execute("SELECT * FROM agents WHERE id = %s",(id,))
        new_agent = cursor.fetchone()
        cursor.close() 
        return new_agent
    
    def get_all_agents(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents")
        agents = cursor.fetchall()
        cursor.close()
        return agents
    
    def get_agent_by_id(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM agents WHERE id= %s",(id,))
        agent = cursor.fetchone()
        cursor.close()
        return agent
    
    def update_agent(self,id:int, data:dict):
        if "id" in data:
            raise IdCannotChengedError
        conn = self.db.get_connection()
        cursor = conn.cursor()
        set_columns = [f"{key}=%s" for key in data.keys()]
        set_clause = ", ".join(set_columns) 
        query = f"""UPDATE agents
                SET {set_clause}
                WHERE id = %s"""
        values = list(data.values())
        cursor.execute(query,values+[id])
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        if updated:
            return f"Agent {id} updated successfully"
        return "Update failed " 

    def deactivate_agent(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor() 
        cursor.execute("UPDATE agents SET is_active=FALSE WHERE id=%s",(id,)) 
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        if updated:
            return f"Agent {id} deactivated successfully"
        return "Deactivate failed"

    def increment_completed(self,id:int):         
        conn = self.db.get_connection()
        cursor = conn.cursor() 
        cursor.execute("UPDATE agents SET completed_missions=completed_missions+1 WHERE id=%s",(id,)) 
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        if updated:
            return f"Agent {id} updated successfully"
        return "Update failed "
    
    def increment_failed(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor() 
        cursor.execute("UPDATE agents SET failed_missions=failed_missions+1 WHERE id=%s",(id,)) 
        conn.commit()
        updated = cursor.rowcount > 0
        cursor.close()
        if updated:
            return f"Agent {id} updated successfully"
        return "Update failed"    

    def get_agent_performance(self,id:int):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT completed_missions AS completed FROM agents WHERE id=%s",(id,))
        completed_dict = cursor.fetchone()
        cursor.execute("SELECT failed_missions AS failed FROM agents WHERE id=%s",(id,))
        failed_dict = cursor.fetchone()
        cursor.close() 
        total_dict = {"total":completed_dict["completed"] + failed_dict["failed"] } 
        try:
            success_rate_dict = {"success_rate":completed_dict["completed"] / total_dict["total"] * 100}
        except ZeroDivisionError:
             success_rate_dict = {"success_rate":0}   
        return completed_dict | failed_dict | total_dict | success_rate_dict
    
    def count_active_agents(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS active_agents FROM agents WHERE is_active=TRUE ")
        active_agents = cursor.fetchone()
        cursor.close()
        return active_agents

db_agent = AgentDB()

