from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from scramble_generator import ScrambleGenerator
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('get_scramble')
def get_scramble():
    scramble_gen = ScrambleGenerator()
    scramble, explanations = scramble_gen.get_scramble_with_explanation()
    socketio.emit('scramble', {
        'scramble': scramble,
        'explanations': explanations
    })

@socketio.on('analyze_solve')
def analyze_solve(data):
    solve_time = data.get('solve_time', 0)
    return {
        'solve_time': f"{solve_time:.2f}",
        'suggestions': [
            "Practice F2L lookahead to reduce pauses",
            "Consider learning advanced PLL algorithms",
            "Work on finger tricks for faster execution"
        ]
    }

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
  
