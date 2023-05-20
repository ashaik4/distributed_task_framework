from flask import Flask, request, jsonify
from tasks import generate_fibonacci
from celery.result import ResultBase
from flask_socketio import SocketIO, emit 
import logging

logging.basicConfig(filename="app_server.log",
                format='%(asctime)s %(message)s',
                filemode='w')
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.DEBUG)
# logger.addHandler(log_handler)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.get_json()

    name = data.get('name')
    age = data.get('age')

    if not name or not age:
        return jsonify({'message': 'Bad Request', 'data': {}, 'status': 'error'}), 400

    return jsonify({'message': 'Data received', 'data': {'name': name, 'age': age}, 'status': 'success'}), 200



@app.route('/api/fibonacci', methods=['POST'])
def fibonacci():
    data = request.get_json()
    nth_fibonacci = int(data.get('n'))
    if not nth_fibonacci: 
        return jsonify({'message': 'Bad Request', 'data': {}, 'status': 'error'}), 400
    #fibonacci_sequence = generate_fibonacci(nth_fibonacci)
    task = generate_fibonacci.delay(nth_fibonacci)
    socketio.emit('log', 'Task ID: {}'.format(str(task.id)))
    socketio.emit('log', 'Result: {}'.format(str(task.get())))
    # socketio.emit('log', 'Result: {}'.format(str([v for v in task.collect() if not isinstance(v, (ResultBase, tuple))])))

    return jsonify({'message': 'Data received', 'data': {'n': nth_fibonacci, 'task_id': str(task.id)}, 'status': 'success'}), 200


@socketio.on('connect')
def handle_connect():
    emit('log', 'Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    emit('log', 'Client disconnected')

@socketio.on('log')
def handle_log(message):
    emit('log', message, broadcast=True)

def log_handler(message):
    socketio.emit('log', message)

if __name__ == '__main__':
    # app.run(debug=True, host='0.0.0.0', port=5001)
    


    socketio.run(app, debug=True, host='0.0.0.0', port=5001)