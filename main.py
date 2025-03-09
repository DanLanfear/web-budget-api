from flask import Flask, jsonify, request
from flask_restx import Resource, Api, fields, marshal_with
import os

app = Flask(__name__)

api = Api(app)


class User:
    fields = {
        'name': fields.String,
        'email': fields.String
    }
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

users = [
    User(0,"daniel", "ddblanfearjr@yahoo.com", "password"),
]


class Hello(Resource):
    def get(self):
        return jsonify({'message':'hello world'})

@api.route('/users')
class UserList(Resource):
    @marshal_with(User.fields)
    def get(self):
        return users

@api.route('/users/<user_id>')
class User(Resource):
    @marshal_with(User.fields)
    def get(self, user_id):
        user = users[int(user_id)]
        return user


api.add_resource(Hello, '/')

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '5000')
    app.run(debug=True, port=server_port, host='0.0.0.0')
