from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory dictionary to store tasks
tasks = {}
task_id_counter = 1

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"}), 200

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(list(tasks.values())), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.get_json()
    
    if not data or 'title' not in data or 'description' not in data:
        return jsonify({"error": "Missing title or description"}), 400
        
    task_id = task_id_counter
    task = {
        "id": task_id,
        "title": data['title'],
        "description": data['description'],
        "created_at": datetime.utcnow().isoformat()
    }
    
    tasks[task_id] = task
    task_id_counter += 1
    
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks.get(task_id)
    if task:
        return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if task_id in tasks:
        del tasks[task_id]
        return jsonify({"message": "Task deleted successfully"}), 200
    return jsonify({"error": "Task not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
