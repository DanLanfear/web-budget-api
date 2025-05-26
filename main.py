from flask import Flask, jsonify, request
from flask_restx import Resource, Api, fields, marshal_with
from models import User, Transaction
from firebase_admin import credentials, firestore, initialize_app


import datetime
import os

app = Flask(__name__)

api = Api(app)
cloud = os.environ.get('cloud')
key_path = '/firebase-key/latest-key' if cloud else 'db_key.json'


cred = credentials.Certificate(key_path)
default_app = initialize_app(cred)
db = firestore.client()

user_fields = {
        'name': fields.String,
        'email': fields.String
    }

transaction_fields = {
    'description': fields.String,
    'date': fields.Date,
    'amount': fields.Fixed(decimals=2),
}

users = db.collection('Users')

transactions =[
    Transaction(0, "kroger", datetime.datetime(2025, 4, 17), 100.00),
    Transaction(1, "gasoline", datetime.datetime(2025, 4, 18), 50.00),
    Transaction(2, "wifi", datetime.datetime(2025, 4, 19), 59.00),
    Transaction(3, "chick fil a", datetime.datetime(2025, 4, 20), 20.00)
]

cards = []

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


class Hello(Resource):
    def get(self):
        return jsonify({'message':'hello world'})

@api.route('/users')
class UserList(Resource):
    @marshal_with(user_fields)
    def get(self):
        try:
            user_ref = db.collection('Users')
            users = [doc.to_dict() for doc in user_ref.stream()]

            return users,200
        except Exception as e:
            return f"An Error Occured: {e}", 400

@api.route('/users/<user_id>')
class User(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        try:
            user_ref = db.collection('Users').document(user_id).get()
            user = user_ref.to_dict()
            return user, 200
        except Exception as e:
            return f"An Error Occured: {e}", 400

    # def delete(self, user_id):
    #     users = db.collections('Users')
    #     user = users[user_id]
    #     # delete user

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
