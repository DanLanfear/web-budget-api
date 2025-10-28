# from flask_restx import Namespace, Resource, fields
# from flask import request

# # Create a namespace for transactions
# api = Namespace('transactions', description='User transaction operations')

# # Define the schema for a single transaction
# transaction_model = api.model('Transaction', {
#     'amount': fields.Float(required=True, description='Transaction amount'),
#     'category_id': fields.Integer(required=True, description='Category ID'),
#     'description': fields.String(required=False, description='Transaction description')
# })

# # Define the schema for bulk input
# bulk_transaction_model = api.model('TransactionBulkInput', {
#     'transactions': fields.List(fields.Nested(transaction_model), required=True, description='List of transactions')
# })


# @api.route('/users/<int:user_id>/transactions/bulk')
# class TransactionBulkResource(Resource):
#     @api.expect(bulk_transaction_model, validate=True)
#     @api.response(201, 'Transactions created successfully')
#     @api.doc(description='Bulk create transactions for a given user')
#     def post(self, user_id):
#         """Bulk create user transactions"""
#         data = request.get_json()
#         transactions = data.get('transactions', [])
#         # Your database logic goes here
#         return {
#             "message": f"Added {len(transactions)} transactions for user {user_id}",
#             "transactions": transactions
#         }, 201
