'''
Module:HCSubscription

Creates the HCSubscription table in GAE.

This table stores the subscription information

Version: 1.0

Created on Dec 16, 2012

Author:
   Farhat Pachisa (farhat@homecampus.com.sg)
   
Copyright:
    Copyright (c) 2012, Home Campus.  All Rights Reserved.

Usage:
'''


from google.cloud import datastore

client = datastore.Client()

def create_hc_subscription(data):
    required_fields = [
        "paypal_token", "student_id", "start_date", "end_date",
        "amount", "period", "status"
    ]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} is required")

    key = client.key("HCSubscription")
    entity = datastore.Entity(key=key)

    entity.update({
        "paypal_token": data["paypal_token"],
        "student_id": data["student_id"],
        "start_date": data["start_date"],
        "end_date": data["end_date"],
        "amount": data["amount"],
        "period": data["period"],
        "status": data["status"],
        "transaction_id": data.get("transaction_id"),
        "email": data.get("email"),
        "country_code": data.get("country_code"),
        "paypal_fee": data.get("paypal_fee"),
        "profile_id": data.get("profile_id"),
        "student_number": data.get("student_number")
    })

    client.put(entity)
    return entity.key




