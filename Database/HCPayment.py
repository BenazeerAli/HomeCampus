'''
Module:HCPayment

Creates the HCPayment table in GAE.

This table stores the subscription information

Version: 1.0

Created on Aug 21, 2013

Author:
   Farhat Pachisa (farhat@homecampus.com.sg)
   
Copyright:
    Copyright (c) 2012, Home Campus.  All Rights Reserved.

Usage:
'''

from google.cloud import datastore

client = datastore.Client()

def create_hcpayment_entity(data):
    key = client.key("HCPayment")
    entity = datastore.Entity(key=key)

    entity.update({
        "transaction_id": data.get("transaction_id"),
        "transaction_type": data.get("transaction_type"),
        "payer_email": data.get("payer_email"),
        "next_payment_date": data.get("next_payment_date"),
        "payer_id": data.get("payer_id"),
        "recurring_payment_id": data.get("recurring_payment_id"),
        "payment_status": data.get("payment_status"),
        "amount": data.get("amount"),
        "paypal_fee": data.get("paypal_fee"),
        "payment_date": data.get("payment_date")
    })

    client.put(entity)
    return entity.key






