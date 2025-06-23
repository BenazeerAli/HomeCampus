'''
Module:HCBooks

Creates the HCBooks table in GAE.

This tables provides user access to HC books

Version: 1.0

Created on Jul 12, 2014

Author:
   Farhat Pachisa (farhat@homecampus.com.sg)
   
Copyright:
    Copyright (c) 2012, Home Campus.  All Rights Reserved.

Usage:
'''

from google.cloud import datastore
from datetime import datetime

client = datastore.Client()

def create_hcbook_entity(data):
    """
    Create a new HCBooks entity with provided data (as a dict).
    """
    key = client.key("HCBooks")
    entity = datastore.Entity(key=key)

    entity.update({
        "book_code": data["book_code"],
        "book_name": data["book_name"],
        "username": data["username"],
        "email": data.get("email"),
        "start_date": data.get("start_date"),  # datetime object
        "end_date": data.get("end_date"),      # datetime object
        "authorized": data.get("authorized", False),
        "amount": data["amount"],
        "status": data.get("status"),
        "paypal_token": data["paypal_token"],
        "transaction_id": data.get("transaction_id"),
        "country_code": data.get("country_code"),
        "paypal_fee": data.get("paypal_fee")
    })

    client.put(entity)
    return entity.key



