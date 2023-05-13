from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS

rest_api_app = Flask(__name__)
CORS(rest_api_app)
rest_api_app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(rest_api_app)

class Person(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


    def json(self):
        return {'id': self.id,'name': self.name,'age': self.age,'gender': self.gender,'email': self.email}

db.create_all()

#create a test route
@rest_api_app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)


# create a person
@rest_api_app.route('/persons', methods=['POST'])
def create_person():
  try:
    data = request.get_json()
    new_person = Person(name=data['name'], age=data['age'], gender=data['gender'], email=data['email'])
    db.session.add(new_person)
    db.session.commit()
    return make_response(jsonify({'message': 'person created'}), 201)
  except e:
    return make_response(jsonify({'message': 'error creating person'}), 500)

# get all persons
@rest_api_app.route('/persons', methods=['GET'])
def get_persons():
  try:
    persons = Person.query.all()
    return make_response(jsonify([person.json() for person in persons]), 200)
  except e:
    return make_response(jsonify({'message': 'error getting persons'}), 500)

# get a person by id
@rest_api_app.route('/persons/<int:id>', methods=['GET'])
def get_person(id):
  try:
    person = Person.query.filter_by(id=id).first()
    if person:
      return make_response(jsonify({'person': person.json()}), 200)
    return make_response(jsonify({'message': 'person not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error getting person'}), 500)

# update a person
@rest_api_app.route('/persons/<int:id>', methods=['PUT'])
def update_person(id):
  try:
    person = Person.query.filter_by(id=id).first()
    if person:
      data = request.get_json()
      person.name = data['name']
      person.age = data['age']
      person.gender = data['gender']
      person.email = data['email']
      db.session.commit()
      return make_response(jsonify({'message': 'person updated'}), 200)
    return make_response(jsonify({'message': 'person not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error updating person'}), 500)

# delete a person
@rest_api_app.route('/persons/<int:id>', methods=['DELETE'])
def delete_person(id):
  try:
    person = Person.query.filter_by(id=id).first()
    if person:
      db.session.delete(person)
      db.session.commit()
      return make_response(jsonify({'message': 'person deleted'}), 200)
    return make_response(jsonify({'message': 'person not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error deleting person'}), 500)