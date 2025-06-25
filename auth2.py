from google.cloud import datastore
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

client = datastore.Client()

class HomeCampusUser:
    KIND = 'HomeCampusUser'

    def __init__(self, entity=None):
        self.entity = entity or datastore.Entity(client.key(self.KIND))

    @classmethod
    def get_by_username(cls, username):
        key = client.key(cls.KIND, username.lower())
        entity = client.get(key)
        return cls(entity) if entity else None

    @classmethod
    def create(cls, username, **kwargs):
        key = client.key(cls.KIND, username.lower())
        if client.get(key):
            return None  # Already exists

        entity = datastore.Entity(key=key)
        now = datetime.datetime.utcnow()

        is_parent = kwargs.get('IsParent', False)
        parent_id_val = kwargs.get('parent_id')

        if is_parent:
            # Parent user: no parent_id
            parent_id_val = None
        else:
            # Child user: parent_id must be a string (e.g., username)
            # If accidentally passed a user object, extract username
            if hasattr(parent_id_val, 'username'):
                parent_id_val = parent_id_val.username
            elif callable(parent_id_val):
                parent_id_val = str(parent_id_val())

        entity.update({
            'username': username,
            'created': now,
            'updated': now,
            'password_hash': kwargs.get('password_hash'),
            'authorized': kwargs.get('authorized', False),
            'active': kwargs.get('active', True),
            'IsParent': is_parent,
            'IsTeacher': kwargs.get('IsTeacher', False),
            'first_name': kwargs.get('first_name'),
            'last_name': kwargs.get('last_name'),
            'parent_first_name': kwargs.get('parent_first_name'),
            'parent_last_name': kwargs.get('parent_last_name'),
            'skill': kwargs.get('skill'),
            'school_code': kwargs.get('school_code'),
            'parent_id': parent_id_val,
        })

        client.put(entity)
        return cls(entity)

        

    def save(self):
        self.entity['updated'] = datetime.datetime.utcnow()
        client.put(self.entity)

    @property
    def username(self):
        return self.entity.get('username')

    @property
    def password_hash(self):
        return self.entity.get('password_hash')

    @property
    def is_teacher(self):
        return self.entity.get('IsTeacher', False)
    def id(self):
        return self.entity.get('username')
    @property
    def is_parent(self):
        return self.entity.get('IsParent', False)

    @classmethod
    def get_by_id(cls, user_id):
        key = client.key(cls.KIND, user_id)
        entity = client.get(key)
        return cls(entity) if entity else None

    def __repr__(self):
        return f"<HomeCampusUser username={self.username}>"
    def get_id(self):
        # Return a unique identifier for this user — Flask-Login uses this internally
        return self.username
    @property
    def is_active(self):
        # You can decide what counts as active. For example:
        return self.entity.get('active', True)

    @property
    def is_authenticated(self):
        # Return True if the user is authenticated
        return True

    @property
    def is_anonymous(self):
        # Return False because this is not an anonymous user
        return False
    @property
    def first_name(self):
        return self.entity.get('first_name')


# Function to get user by username
def get_user_by_username(username):
    user = HomeCampusUser.get_by_username(username)
    return user

def get_user_by_id(user_id):
    return HomeCampusUser.get_by_id(user_id)

# Function to create user with password hashing
def create_user(username, password, **kwargs):
    password_hash = generate_password_hash(password)
    user = HomeCampusUser.create(
        username=username,
        password_hash=password_hash,
        **kwargs
    )
    return user

# Function to check user password
def check_user_password(user, password):
    if not user:
        return False
    return check_password_hash(user.password_hash, password)

# Function to get child users for a given parent id
def get_child_users_for_parent(parent_id):
    query = client.query(kind=HomeCampusUser.KIND)
    query.add_filter('parent_id', '=', parent_id)
    entities = list(query.fetch())
    return [HomeCampusUser(entity) for entity in entities]



