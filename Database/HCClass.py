'''
Module:HCClass

Creates the HCClass table in GAE.

This tables stores the class information.

Version: 1.0

Created on Sep 09, 2013

Author:
   Farhat Pachisa (farhat@homecampus.com.sg)
   
Copyright:
    Copyright (c) 2012, Home Campus.  All Rights Reserved.

Usage:
'''

from google.cloud import datastore
from datetime import datetime

client = datastore.Client()

def create_hcclass_entity(data):
    """
    Creates a new HCClass entity in Datastore.
    
    Expected keys in `data` dict:
    - teacher_username (str)
    - class_name (str)
    - class_skill (str, optional)
    """
    key = client.key("HCClass")
    entity = datastore.Entity(key=key)

    entity.update({
        "teacher_username": data["teacher_username"],
        "class_name": data["class_name"],
        "class_skill": data.get("class_skill"),
        "create_date": datetime.utcnow()  # auto_now=True equivalent
    })

    client.put(entity)
    return entity.key



