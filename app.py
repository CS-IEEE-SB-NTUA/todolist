from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


'''
Den xerw an tha exoume xrono na to exigisoume auto alla tha mporousame na
ylopiisoume tin klasi mprosta tous kai na tous poume na kanoun autoi ta crud commands me tin lista
px gia to spiti i kt na exikiothoune 
kai dld tous dixnoume pws doulevoun ta migrations as well 
class TodoListModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    todos = db.relationship('TodoModel', backref='list', lazy=True)

    def __repr__(self):
        return f"<TodoList {self.id}: {self.name}>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'todos': [todo.to_dict() for todo in self.todos]
        }
'''

# To-do model
class TodoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Todo {self.id}: {self.title}>"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }

# Route to get a specific todo ( as to see the database )
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    with app.app_context():
        todo = TodoModel.query.get(todo_id)
        if todo:
            return jsonify(todo.to_dict())
        else:
            return jsonify({'message': 'To-do not found'}), 404

# Route to create a new todo
@app.route('/todos', methods=['POST'])
def create_todo():
    with app.app_context():
        todo = TodoModel(title=request.form['title'], description=request.form['description'])
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('todo_list'))


# Route to update an existing todo 
@app.route('/todos/<int:todo_id>', methods=['PUT', 'POST'])
def update_todo(todo_id):
    with app.app_context():
        todo = TodoModel.query.get(todo_id)
        if todo:
            todo.title = request.form.get('title', todo.title)
            todo.description = request.form.get('description', todo.description)
            completed = request.form.get('completed', '')
            if completed == 'on':
                todo.completed = True
            else:
                todo.completed = False
            db.session.commit()
            return redirect(url_for('todo_list'))
        else:
            return jsonify({'message': 'To-do not found'}), 404


# Route to delete a specific todo 
@app.route('/todos/delete/<int:todo_id>', methods=['DELETE', 'POST'])
def delete_todo(todo_id):
    with app.app_context():
        todo = TodoModel.query.get(todo_id)
        try:
            db.session.delete(todo)
            db.session.commit()
            return redirect('/')
        except:
            return 'Error: to-do not found'

# Home route
@app.route('/', methods=['GET'])
def todo_list():
    with app.app_context():
        todos= TodoModel.query.all()
        return render_template('todo_list.html', todos=todos)

# Route to display the new to-do form
@app.route('/todos/new', methods=['GET'])
def new_todo():
    return render_template('new_todo.html')

# Route to display the edit to-do form
@app.route('/todos/<int:todo_id>/edit', methods=['GET'])
def edit_todo_form(todo_id):
    with app.app_context():
        todo = TodoModel.query.get(todo_id)
        if todo:
            return render_template('edit_todo.html', todo=todo)
        else:
            return jsonify({'message': 'To-do not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
