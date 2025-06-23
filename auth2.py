from google.cloud import datastore
from flask_login import UserMixin
import hashlib

client = datastore.Client(project='homecampus-flask')

class User(UserMixin):
    def __init__(self, user_id, username, password_hash, is_parent=False, first_name='', parent_id=None):
        self.id = user_id
        self.username = username
        self.password_hash = password_hash
        self.is_parent = is_parent
        self.first_name = first_name
        self.parent_id = parent_id


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
        password_hash=user_entity['password_hash'],
        is_parent=user_entity.get('is_parent', True),
        first_name=user_entity.get('first_name', ''),
        parent_id=user_entity.get('parent_id')
    )

def get_user_by_id(user_id):
    key = client.key('User', int(user_id))
    user_entity = client.get(key)
    if not user_entity:
        return None
    return User(
        user_id=str(user_entity.key.id),
        username=user_entity['username'],
        password_hash=user_entity['password_hash'],
        is_parent=user_entity.get('is_parent', True),
        first_name=user_entity.get('first_name', ''),
        parent_id=user_entity.get('parent_id')
    )

def create_user(username, password, is_parent=False, first_name='', parent_id=None):

    if get_user_by_username(username):
        return None  # User exists
    user_entity = datastore.Entity(key=client.key('User'))
    user_entity.update({
        'username': username,
        'password_hash': hash_password(password),
        'is_parent': is_parent,
        'first_name': first_name
    })
    if not is_parent and parent_id:
        user_entity['parent_id'] = int(parent_id)

    client.put(user_entity)

    return User(
        user_id=str(user_entity.key.id),
        username=username,
        password_hash=user_entity['password_hash'],
        is_parent=is_parent,
        first_name=first_name,
        parent_id=user_entity.get('parent_id')
    )
def get_child_users_for_parent(parent_id):
    query = client.query(kind='User')
    query.add_filter('is_parent', '=', False)
    query.add_filter('parent_id', '=', int(parent_id))
    children = []
    for entity in query.fetch():
        children.append(User(
            user_id=str(entity.key.id),
            username=entity['username'],
            password_hash=entity['password_hash'],
            is_parent=False,
            first_name=entity.get('first_name', ''),
            parent_id=entity.get('parent_id')
        ))
    return children
