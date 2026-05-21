from datetime import datetime
# pyrefly: ignore [missing-import]
from flask_sqlalchemy import SQLAlchemy

# Instantiate SQLAlchemy. We will bind this to our Flask app in app.py.
db = SQLAlchemy()

class Task(db.Model):
    """
    Task Database Model
    Defines the structure of the 'task' table in SQLite.
    """
    __tablename__ = 'tasks'

    # Primary key: Unique identifier for each task
    id = db.Column(db.Integer, primary_key=True)
    
    # Task title: Text, maximum 100 characters, required
    title = db.Column(db.String(100), nullable=False)
    
    # Task description: Text, optional (nullable)
    description = db.Column(db.String(200), nullable=True)
    
    # Task completion status: Boolean, defaults to False (incomplete)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    
    # Creation timestamp: Automatically populated when a task is created
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Task {self.id}: {self.title} (Completed: {self.completed})>"
