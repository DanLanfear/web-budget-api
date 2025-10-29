from flask_restx import Api
from resources.transaction import api as transactions_ns

def register_routes(app):
    api = Api(app, version='1.0', title='Finance API', description='User Transactions API')
    # api.add_namespace(users_ns, path='/api/v1')
    api.add_namespace(transactions_ns)
    # api.add_namespace(categories_ns, path='/api/v1')

    return api