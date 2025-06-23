'''
Created on Jan 14, 2011

@author: Farhat
'''
from google.cloud import datastore

client = datastore.Client()

def delete_problems_table_records(limit=1000):
    query = client.query(kind="ProblemsTable")
    entities = list(query.fetch(limit=limit))
    if entities:
        keys = [entity.key for entity in entities]
        client.delete_multi(keys)

