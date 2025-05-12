from flask import Flask, jsonify, request
from flask_restx import Resource, Api, fields, marshal_with
from models import User, Transaction

import datetime
import os

app = Flask(__name__)

api = Api(app)

user_fields = {
        'name': fields.String,
        'email': fields.String
    }

transaction_fields = {
    'description': fields.String,
    'date': fields.Date,
    'amount': fields.Fixed(decimals=2),
}

users = [
    User(0,"daniel", "ddblanfearjr@yahoo.com", "password")
]

transactions =[
    Transaction(0, "kroger", datetime.datetime(2025, 4, 17), 100.00),
    Transaction(1, "gasoline", datetime.datetime(2025, 4, 18), 50.00),
    Transaction(2, "wifi", datetime.datetime(2025, 4, 19), 59.00),
    Transaction(3, "chick fil a", datetime.datetime(2025, 4, 20), 20.00)
]

cards = []


class Hello(Resource):
    def get(self):
        return jsonify({'message':'hello world'})

@api.route('/users')
class UserList(Resource):
    @marshal_with(user_fields)
    def get(self):
        return users

@api.route('/users/<user_id>')
class User(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = users[int(user_id)]
        return user
    def delete(self, user_id):
        user = users[int(user_id)]
        # delete user

@api.route('/transactions')
class TransactionList(Resource):
    @marshal_with(transaction_fields)
    def get(self):
        return transactions


@api.route('/transactions/<transaction_id>')
class Transaction(Resource):
    @marshal_with(transaction_fields)
    def get(self, transaction_id):
        transaction = transactions[int(transaction_id)]
        return transaction


api.add_resource(Hello, '/')


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '5000')
    app.run(debug=True, port=server_port, host='0.0.0.0')
