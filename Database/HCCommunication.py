'''
Module:HCCommunication

Creates the communication table in GAE.

This tables stores all the communication email information sent to the user.

Version: 1.0

Created on May 23, 2013

Author:
   Farhat Pachisa (farhat@homecampus.com.sg)
   
Copyright:
    Copyright (c) 2012, Home Campus.  All Rights Reserved.

Usage:
'''

from google.cloud import datastore
from datetime import datetime

client = datastore.Client()

def create_hccommunication_entity(data):
    """
    Creates a new HCCommunication entity in Datastore.

    Expected keys in `data` dict:
    - email (str)
    - UnsubscriptionKey (str)
    - LastCommunicationKey (str)  # required
    - ActiveUnsubscribedReportdate (datetime, optional)
    - UnfinishedWorksheetReportdate (datetime, optional)
    - IncompleteTransactionReportdate (datetime, optional)
    - unsubscribed (bool, optional)
    """
    # Validate required field
    if "LastCommunicationKey" not in data:
        raise ValueError("LastCommunicationKey is required")

    key = client.key("HCCommunication")
    entity = datastore.Entity(key=key)

    entity.update({
        "email": data.get("email"),
        "UnsubscriptionKey": data.get("UnsubscriptionKey"),
        "unsubscribed": data.get("unsubscribed", False),
        "LastCommunicationKey": data["LastCommunicationKey"],
        "UpdateDate": datetime.utcnow(),  # auto_now=True equivalent
        "ActiveUnsubscribedReportdate": data.get("ActiveUnsubscribedReportdate"),
        "UnfinishedWorksheetReportdate": data.get("UnfinishedWorksheetReportdate"),
        "IncompleteTransactionReportdate": data.get("IncompleteTransactionReportdate")
    })

    client.put(entity)
    return entity.key




