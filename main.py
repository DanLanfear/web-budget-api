from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import os

app = Flask(__name__)

api = Api(app)

class Hello(Resource):
    def get(self):
        return jsonify({'message':'hello world'})
    

api.add_resource(Hello,'/')

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '5000')
    app.run(debug=True, port=server_port, host='0.0.0.0')