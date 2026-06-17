import mysql.connector

class DB_connection:
    def __init__(self):
        self.connect()
    
    def connect(self):
        self.connection = mysql.connector.connect(host="localhost",user="root",password="1234")

    def get_connection(self):
        if not self.connection.is_connected():
            self.connect()
        return self.connection  

    def create_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")  
        cursor.execute("USE Intelligence_db")    
        cursor.close()

    def create_tables(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS agents(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       name VARCHAR(50) NOT NULL,
                       specialty VARCHAR(50) NOT NULL,
                       is_active BOOLEAN DEFAULT TRUE NOT NULL,
                       completed_missions INT DEFAULT 0 NOT NULL,
                       failed_missions INT DEFAULT 0 NOT NULL,
                       agent_rank ENUM('Junior', 'Senior', 'Commander') NOT NULL
                       )""")
        
        cursor.execute("""CREATE TABLE IF NOT EXISTS missions(
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       title VARCHAR(50) NOT NULL,
                       description TEXT NOT NULL,
                       location VARCHAR(50) NOT NULL,
                       difficulty INT NOT NULL,
                       importance INT NOT NULL,
                       status VARCHAR(50) DEFAULT 'NEW' NOT NULL,
                       risk_level VARCHAR(50) NOT NULL,
                       assigned_agent_id INT NULL
                       )""")
        cursor.close()
    
    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close() 

db = DB_connection()

