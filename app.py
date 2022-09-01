from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)



class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)


if not os.path.exists('test.db'):
    db.create_all()


@app.route('/')
def index():
    return jsonify({'message': 'Hello World'})


# Get all users

@app.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()
    if not users:
        return jsonify({'message': 'No user found!'})
    user_list = {}
    for user in users:
        user_list[user.id] = {'name': user.name, 'email': user.email}
    return jsonify({'users': user_list})

# Get a single user

@app.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'No user found!'})
    user = {'name': user.name, 'email': user.email}
    return jsonify({'user': user})

# Create a new user

@app.route('/user', methods=['POST'])
def create_user():
    name, email = request.json['name'], request.json['email']
    if not name or not email:
        return jsonify({'message': 'Missing arguments'}), 400
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'})

# Update user

@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    name, email = request.json['name'], request.json['email']
    if not name or not email:
        return jsonify({'message': 'Missing arguments'}), 400
    elif not User.query.get(id):
        return jsonify({'message': 'No user found!'})
    user = User.query.get(id)
    user.name = name
    user.email = email
    db.session.commit()
    return jsonify({'message': 'User updated'})

# Delete user

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})


# Get all exercises

app.route('/exercise', methods=['GET'])
def get_all_exercise():
    exercise = Exercise.query.all()
    if not exercise:
        return jsonify({'message': 'No exercise found'}), 404
    exercise_list = {}
    for ex in exercise:
        exercise_list[ex.id] = {'name': ex.name,
                             'description': ex.description}
    return jsonify({'exercise': exercise_list})

# Get one exercise

@app.route('/exercise/<int:id>', methods=['GET'])
def get_one_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'message': 'No exercise found'}), 404
    exercise = {'name': exercise.name,
                 'description': exercise.description}
    return jsonify({'exercise': exercise})


# Create exercise

@app.route('/exercise', methods=['POST'])
def create_exercise():
    name, description=request.json[
        'name'], request.json['description']
    if not name or not description:
        return jsonify({'message': 'Missing arguments'}), 400
    exercise = Exercise(name=name,
                          description=description)
    db.session.add(exercise)
    db.session.commit()
    return jsonify({'message': 'exercise created'})

# Update exercise

@app.route('/exercise/<int:id>', methods=['PUT'])
def update_exercise(id):
    exercise = Exercise.query.get(id)
    name, description = request.json[
        'name'], request.json['description']
    if not name or not description:
        return jsonify({'message': 'Missing arguments'}), 400
    elif not exercise.query.get(id):
        return jsonify({'message': 'exercise not found'}), 404

    exercise.name = name
    exercise.description = description
    db.session.commit()
    return jsonify({'message': 'exercise updated'})


# Delete exercise
@app.route('/exercise/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return jsonify({'message': 'Not Found'})
    db.session.delete(exercise)
    db.session.commit()
    return jsonify({'message': 'exercise deleted'})




if __name__ == '__main__':
    app.run(debug=True)
