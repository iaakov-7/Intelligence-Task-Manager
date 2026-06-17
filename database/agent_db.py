from db_connection import db

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
        cursor = conn.cursor()
        pass
    
db_agent = AgentDB()
db.create_database()
