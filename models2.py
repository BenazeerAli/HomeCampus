from google.cloud import datastore
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

        # Required base fields
        entity.update({
            'username': username,
            'created': now,
            'updated': now,
            'password_hash': kwargs.get('password_hash'),
            'authorized': kwargs.get('authorized', False),
            'active': kwargs.get('active', True),
            'IsParent': kwargs.get('IsParent', False),
            'IsTeacher': kwargs.get('IsTeacher', False),
            'first_name': kwargs.get('first_name'),
            'last_name': kwargs.get('last_name'),
            'parent_first_name': kwargs.get('parent_first_name'),
            'parent_last_name': kwargs.get('parent_last_name'),
            'skill': kwargs.get('skill'),
            'school_code': kwargs.get('school_code'),
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

    @property
    def is_parent(self):
        return self.entity.get('IsParent', False)

    def __repr__(self):
        return f"<HomeCampusUser username={self.username}>"
