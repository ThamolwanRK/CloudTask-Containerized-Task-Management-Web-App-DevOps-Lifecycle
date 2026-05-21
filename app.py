import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Task

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
# We save the database file 'tasks.db' inside the 'instance' folder of the project.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key is required for using flash messages to notify users
app.config['SECRET_KEY'] = 'dev-key-for-university-project-123'

# Bind the database instance to this Flask application
db.init_app(app)

# Ensure the database tables are created before handling any request
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """
    Main Route: Renders the dashboard and the list of tasks.
    It calculates stats like total, completed, pending tasks and completion rate.
    """
    # Fetch all tasks from SQLite, ordered by creation date (newest first)
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    
    # Calculate statistics for the dashboard
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.completed)
    pending_tasks = total_tasks - completed_tasks
    
    # Calculate completion percentage (handle division by zero if there are no tasks)
    completion_rate = round((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0

    return render_template(
        'index.html', 
        tasks=tasks, 
        total_tasks=total_tasks, 
        completed_tasks=completed_tasks, 
        pending_tasks=pending_tasks, 
        completion_rate=completion_rate
    )

@app.route('/add', methods=['POST'])
def add_task():
    """
    Add Task Route: Handles POST request from the form to create a new task.
    """
    # Get form data
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()

    # Basic input validation
    if not title:
        flash('Task title is required!', 'danger')
        return redirect(url_for('index'))

    # Create a new Task object
    new_task = Task(title=title, description=description)

    try:
        # Add to session and save to SQLite database
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding task: {str(e)}', 'danger')

    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    """
    Toggle Task Status Route: Marks a task as completed or incomplete.
    """
    task = Task.query.get_or_404(task_id)
    
    # Flip the completion status
    task.completed = not task.completed

    try:
        db.session.commit()
        status_text = "completed" if task.completed else "active"
        flash(f'Task marked as {status_text}!', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating task: {str(e)}', 'danger')

    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """
    Delete Task Route: Permanently deletes a task from the database.
    """
    task = Task.query.get_or_404(task_id)

    try:
        # Remove from database session and commit
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'warning')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting task: {str(e)}', 'danger')

    return redirect(url_for('index'))

if __name__ == '__main__':
    # Run Flask server locally on port 5000 in development mode
    app.run(host='0.0.0.0', port=5000, debug=True)
