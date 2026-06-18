# Intelligence-Task-Manager

## System description
Intelligence-Task-Manager is a system created to help an intelligence unit named ShadowNet 
with agent and task management, 
The system has all the necessary actions such as adding a new agent or updating a task status.

## Folder structure
```
intelligence-task-manager/
├── database/
│   ├── db_connection.py
|   |── db_exceptions.py
│   ├── agent_db.py
│   └── mission_db.py
├── routes/
│   ├── agent_routes.py
|   |── mission_routes.py
│   └── report_routes.py
├── utils/
│   └── models.py
|── logs/
|   └── logger_config.py                 
│   └── app.log 
├── main.py  
├── README.md
├── requirements.txt
└── .gitignore
```

## Table structure
### agents
```
id: int, auto_increment, pk
name: varchar
specialty: varchar
is_active: boolean
completed_missions: int
failed_missions: int
agent_rank: enum
```
### missions
```
id: int, auto_increment, pk
title: varchar
description: text
location: varchar
diffculty: int
importance: int
status: varchar
risk_level: varchar
assigned_agent_id: int
```
## Explanation of the classes
### DB_connection 
The class is responsible for connecting to the database and creating the db and tables.
#### Methods:
```
get_connection() / Returns an active connection to MySQL.
create_database() / Creates Intelligence_db if it does not exist.
create_tables() / Creates both tables if they do not exist.
```
### AgentDB
The class is responsible for all SQL operations against the agents table.
#### Methods:
```
create_agent(data) / Creates a new agent and returns the agent object.
get_all_agents() / Returns a list of all agents.
get_agent_by_id(id) / Returns one agent by ID, or None.
update_agent(id, data) / Updates the line, unable to change ID.
deactivate_agent(id) / Sets agent inactive status.
increment_completed(id) / Updates the number of tasks completed.
increment_failed(id) / Updates the number of failed tasks.
get_agent_performance(id) / Returns a dictionary with these keys: total, failed, completed, success_rate.
count_active_agents() / Returns the number of active agents.
```
### MissionDB
The class is responsible for all SQL operations against the missions table.
#### Methods:
```
create_mission(data) / 	Creates a new task and returns the entire object.
get_all_missions() / Returns all tasks.	
get_mission_by_id(id) / Returns one task by ID, or None.
assign_mission(m_id, a_id) / Assigning a task to an agent.
update_mission_status(id, status) / Used for any status change.	
get_open_missions_by_agent(id) / Returns agent ASSIGNED/IN_PROGRESS tasks.
count_all_missions() / total tasks.	
count_by_status(status) / Counting by a certain status.	
count_open_missions() / Counting the open tasks.	
count_critical_missions() / Counting critical tasks. 	
get_top_agent() / The agent with the highest completed_missions
```

## System rules
1. rank must be Junior / Senior / Commander — any other value throws an error.
2. difficulty and importance must be between 1 and 10 — otherwise an error.
3. risk_level is calculated automatically when creating a task — the user does not submit it.
4. An agent with is_active=False cannot accept tasks.
5. An agent cannot have more than 3 open tasks (ASSIGNED / IN_PROGRESS) at the same time.
6. If risk_level=CRITICAL — only an agent with the Commander rank can accept the task.
7. Only a task with the status NEW can be assigned. After assignment: status=ASSIGNED.
8. Only a task with the status ASSIGNED can be started. After: status=IN_PROGRESS.
9. Only a task with the status IN_PROGRESS can be finished and changed to failed or completed.
10. Only a task with the status NEW or ASSIGNED can be canceled — otherwise an error.
 
## Running instructions
- docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0 

- pip install requirements.txt

- uvicorn main:app
  