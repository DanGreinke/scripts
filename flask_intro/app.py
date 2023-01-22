from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# references the current file
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' #3 slashes is relative path, 4 is absolute
#initialize database
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<task %r>' % self.id
    #after creating database, go to python3 shell, with venv active, and type
    #>> from app import db
    #>> db.create_all() [database is created in app's folder]


# prevent a 404 by setting up a route
@app.route('/', methods=['POST','GET']) #Methods let us add data to db and retrieve data from db
def index():
    if request.method == 'POST':
        task_content = request.form['content'] #'content' corresponds to text input id, 'content'
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/') #redirect to homepage
        except:
            return 'There was an issue adding your task :('
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task :('

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating this task :('
    else:
        return render_template('update.html', task=task)

if __name__== "__main__":
    app.run(debug=True)