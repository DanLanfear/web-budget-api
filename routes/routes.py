from flask_restx import Api

def register_routes(app):
    api = Api(app, version='1.0', title='Finance API', description='User Transactions API')
    
    # api.add_namespace(users_ns, path='/api/v1')
    # api.add_namespace(transactions_ns, path='/api/v1')
    # api.add_namespace(categories_ns, path='/api/v1')

    return api