from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define Task Model
class Task(db.Model):
    __tablename__ ='tasks'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    done = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f"<Task {self.task}>"