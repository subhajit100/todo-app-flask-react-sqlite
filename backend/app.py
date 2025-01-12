from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__, static_folder="../frontend/build", static_url_path="")
app.url_map.strict_slashes = False
CORS(app)


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the app with the extension
db.init_app(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }

# Backend API routes 
# Create a new todo
@app.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    new_todo = Todo(
        title=data.get('title'),
        description=data.get('description')
    )
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.__repr__()), 201

# Get all todos
@app.route('/api/todos', methods=['GET', 'OPTIONS'])
def get_todos():
    if request.method == 'OPTIONS':
        return '', 200  # Preflight response
    todos = Todo.query.all()
    return jsonify([todo.__repr__() for todo in todos]), 200

# Get a single todo
@app.route('/api/todos/<int:id>', methods=['GET'])
def get_todo(id):
    todo = Todo.query.get_or_404(id)
    return jsonify(todo.__repr__()), 200

# Update a todo
@app.route('/api/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    data = request.get_json()
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    db.session.commit()
    return jsonify(todo.__repr__()), 200

# Delete a todo
@app.route('/api/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "Todo deleted successfully"}), 200

# Frontend React App will be served at /
@app.route("/")
def serve():
    return send_from_directory(app.static_folder, "index.html")

def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()
    app.run(debug=True)