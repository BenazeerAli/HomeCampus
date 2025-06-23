from google.cloud import datastore
from flask_login import UserMixin
import hashlib

client = datastore.Client(project='homecampus-flask')

class User(UserMixin):
    def __init__(self, user_id, username, password_hash):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash

from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password):
    return generate_password_hash(password)


def get_user_by_username(username):
    query = client.query(kind='User')
    query.add_filter('username', '=', username)
    results = list(query.fetch(limit=1))
    if not results:
        return None
    user_entity = results[0]
    return User(
        user_id=str(user_entity.key.id),
        username=user_entity['username'],
        password_hash=user_entity['password_hash']
    )

def get_user_by_id(user_id):
    key = client.key('User', int(user_id))
    user_entity = client.get(key)
    if not user_entity:
        return None
    return User(
        user_id=str(user_entity.key.id),
        username=user_entity['username'],
        password_hash=user_entity['password_hash']
    )

def create_user(username, password):
    if get_user_by_username(username):
        return None  # User exists
    
    key = client.key('User')
    user_entity = datastore.Entity(key=key)
    user_entity.update({
        'username': username,
        'password_hash': hash_password(password)
    })
    client.put(user_entity)
    return User(user_id=str(user_entity.key.id), username=username, password_hash=user_entity['password_hash'])
