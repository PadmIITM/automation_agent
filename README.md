#Clone the repo
git clone <repository-url>
# 
cd <repository-folder>

# run agent
python3 automation_agent.py

# Give imput to the and get results

curl -X POST http://127.0.0.1:8000/task -H "Content-Type: application/json" -d '{"task": "example_task"}'

