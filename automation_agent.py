from flask import Flask, request, jsonify
from task_handler import execute_task

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Automation Agent is running! Use /run to execute tasks."})
@app.route('/run', methods=['POST'])
def run_task():
    task_desc = request.json.get('task')
    if not task_desc:
        return jsonify({"error": "Missing task description"}), 400

    try:
        result = execute_task(task_desc)
        print(result)
        return jsonify({"status": "success", "message": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
