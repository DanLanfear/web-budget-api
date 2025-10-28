import os
from firebase_admin import credentials, firestore, initialize_app

cloud = os.environ.get('cloud')
key_path = '/firebase-key/latest-key' if cloud else 'db_key.json'


cred = credentials.Certificate(key_path)
default_app = initialize_app(cred)
db = firestore.client()