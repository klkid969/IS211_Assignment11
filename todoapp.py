import pickle
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Save file configuration
TODO_FILE = "todos.pkl"

def save_todos():
    """Save tasks to a file"""
    with open(TODO_FILE, 'wb') as f:
        pickle.dump(todos, f)

def load_todos():
    """Load tasks from file if exists"""
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'rb') as f:
            return pickle.load(f)
    return []  # Return empty list if no file exists

# Initialize todos list by loading from file
todos = load_todos()

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/submit', methods=['POST'])
def submit():
    task = request.form['task']
    email = request.form['email']
    priority = request.form['priority']
    
    todos.append({
        'task': task,
        'email': email,
        'priority': priority
    })
    save_todos()  # Auto-save after adding
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear():
    todos.clear()
    save_todos()  # Auto-save after clearing
    return redirect(url_for('index'))

# NEW: Manual save route (optional but recommended)
@app.route('/save', methods=['POST'])
def manual_save():
    save_todos()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(port=5001, debug=True)