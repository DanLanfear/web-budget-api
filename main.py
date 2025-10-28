from flask import Flask, jsonify, request
from flask_restx import Resource, Api, fields, marshal_with
from models import User, Transaction
from database_constants import transaction_collection, transaction_date
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime
import util

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
    
    def post(self):
        # TODO: write method
        pass

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

    def put(self, user_id):
        # TODO: write method
        pass

    def delete(self, user_id):
        # TODO: write method
        pass


@api.route('/users/<user_id>/transactions')
class TransactionListResource(Resource):
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
                entry['date'] = datetime.strptime(entry['date'], "%Y-%m-%d")
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
    
    def put(self, transaction_id):
        # TODO: write method
        pass

    def delete(self, transaction_id):
        # TODO: write method
        pass

@api.route('/users/<user_id>/transactions/summary')
class TransactionSummaryResource(Resource):
    def get(self, user_id):
       
        # format of MM-YYYY
        start_arg = request.args.get('start').split('-')
        end_arg = request.args.get('end','').split('-')
        start_month = int(start_arg[0])
        start_year = int(start_arg[1])

        if end_arg == '':
            end_month = int(end_arg[0])
            end_year = int(end_arg[1])   
        elif start_month == 12:
            end_month = 1
            end_year = start_year + 1
        else:
            end_month = start_month + 1
            end_year = start_year

        months = util.list_months(start_year,start_month, end_year, end_month)

        start_time = datetime(start_year, start_month, 1, 0, 0, 0)
        end_time = datetime(end_year, end_month, 1, 0, 0, 0)

        transaction_stream = db.collection(transaction_collection)\
            .where('user_id', '==', user_id)\
            .where(transaction_date, '>=', start_time)\
            .where(transaction_date, '<', end_time).stream()
        
        transaction_list = []
        summary = {}

        for item in transaction_stream:
            transaction = Transaction.from_dict(item.to_dict())
            transaction_list.append(transaction)

        for month in months:
            # get the transactions for month
            month_summary = {}
            month_transactions = []
            for transaction in transaction_list:
                if transaction.date.month == month[1] and transaction.date.year == month[0]:
                    month_transactions.append(transaction)
            # create a month summary for all the transactions in that month
            # TODO change keys to use the categories in the DB
            for transaction in month_transactions:
                if transaction.category in list(month_summary.keys()):
                    month_summary[transaction.category] += transaction.amount
                else:
                    month_summary[transaction.category] = transaction.amount
            # add the month summary to the big summary
            summary[f'{month[1]}-{month[0]}'] = month_summary

        # update to upload by month
        # for item in transaction_stream:
        #     transaction = Transaction.from_dict(item.to_dict())
        #     if transaction.category in list(summary.keys()):
        #         summary[transaction.category] += transaction.amount
        #     else:
        #         summary[transaction.category] = transaction.amount
        return summary, 200


if __name__ == '__main__':
    server_port = os.environ.get('PORT', '5000')
    app.run(debug=True, port=server_port, host='0.0.0.0')
