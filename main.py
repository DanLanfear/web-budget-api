from flask import Flask, jsonify, request
from flask_restx import Resource, Api, fields, marshal_with
from models import User, Transaction
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime


import datetime
import os

app = Flask(__name__)

api = Api(app)
cloud = os.environ.get('cloud')
key_path = '/firebase-key/latest-key' if cloud else 'db_key.json'


cred = credentials.Certificate(key_path)
default_app = initialize_app(cred)
db = firestore.client()


transaction_fields = {
    'description': fields.String,
    'date': fields.Date,
    'amount': fields.Fixed(decimals=2),
    'category': fields.String
}
user_fields = {
        'name': fields.String,
        'email': fields.String,
    } 

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
            return users, 200
        except Exception as e:
            return f"An Error Occured: {e}", 400

@api.route('/users/<user_id>')
class UserResource(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        try:
            user_doc_ref = db.collection("Users").document(user_id)
            user = user_doc_ref.get()
            if not user.exists:
                return jsonify({'message':'user not found'}), 404
            return user.to_dict(), 200
        except Exception as e:
            return f"An Error Occured: {e}", 400

    def delete(self, user_id):
        pass


@api.route('/transactions/<transaction_id>')
class TransactionResource(Resource):
    @marshal_with(transaction_fields)
    def get(self, transaction_id):
        try:
            transaction_ref = db.collection("transactions").document(transaction_id)
            transaction = transaction_ref.get()
            if not transaction.exists:
                return jsonify({'message':'transaction not found'}), 404
            return transaction.to_dict(), 200
        except Exception as e:
            return f"An Error Occured: {e}", 400

@api.route('/users/<user_id>/transactions')
class UserTransactionListResource(Resource):
    @marshal_with(transaction_fields)
    def get(self, user_id):
        transaction_stream = db.collection('transactions').where('user_id', '==', user_id).stream()
        transaction_list = []
        for item in transaction_stream:
            transaction = Transaction.from_dict(item.to_dict())
            transaction_list.append(transaction.to_dict())
        return transaction_list, 200
    
    @api.expect([transaction_fields], validate=True)
    def post(self, user_id):
        batch = db.batch()
        for entry in request.get_json():
            transaction_ref = db.collection('transactions').document()
            try:
                entry['date'] = datetime.datetime.strptime(entry['date'], "%Y-%m-%d")
            except ValueError:
                return {'error': 'Invalid date format. Use YYYY-MM-DD.'}, 400
            transaction = Transaction(entry['description'],
                                       entry['date'], 
                                       entry['amount'], 
                                       entry['category'],
                                       user_id)
            batch.set(transaction_ref, transaction.to_dict())
        batch.commit()
        return 201


@api.route('/users/<user_id>/transactions/<transaction_id>')
class UserTransactionResource(Resource):
    @marshal_with(transaction_fields)
    def get(self, user_id, transaction_id):
        pass

    def put(self, user_id, transaction_id):
        pass
    
    def delete(self, user_id, transaction_id):
        pass


api.add_resource(Hello, '/')


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '5000')
    app.run(debug=True, port=server_port, host='0.0.0.0')
