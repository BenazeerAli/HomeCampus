'''
Module:HCResetPassword

Creates the HCResetPassword table in GAE.

This tables stores the reset password link.

Version: 1.0

Created on Feb 24, 2014

Author:
   Farhat Pachisa (farhat@homecampus.com.sg)
   
Copyright:
    Copyright (c) 2012, Home Campus.  All Rights Reserved.

Usage:
'''

from google.cloud import datastore
from datetime import datetime

client = datastore.Client()

def create_reset_password_entity(data):
    required_fields = ["username", "email", "reset_key", "expiry_date"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} is required")

    key = client.key("HCResetPassword")
    entity = datastore.Entity(key=key)

    entity.update({
        "username": data["username"],
        "email": data["email"],
        "reset_key": data["reset_key"],
        "IsChild": data.get("IsChild", False),
        "IsParent": data.get("IsParent", False),
        "create_date": datetime.utcnow(),
        "expiry_date": data["expiry_date"],
        "password_changed": data.get("password_changed", False)
    })

    client.put(entity)
    return entity.key





