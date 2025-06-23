'''
Module:TestsMaster

Creates the tests master table in GAE.

This tables stores all the master information of the test.

Version: 1.0

Created on May 18, 2012

Author:
   Farhat Pachisa (farhat@homecampus.com.sg)
   
Copyright:
    Copyright (c) 2012, Home Campus.  All Rights Reserved.

Usage:
'''

from google.cloud import datastore
from datetime import datetime

client = datastore.Client()

def create_tests_master(data):
    required_fields = [
        "test_id", "test_name", "student_id", "grade",
        "concept", "created_by", "questions"
    ]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} is required")

    key = client.key("TestsMasterTable")
    entity = datastore.Entity(key=key)

    entity.update({
        "test_id": data["test_id"],
        "test_name": data["test_name"],
        "student_id": data["student_id"],
        "grade": data["grade"],
        "concept": data["concept"],
        "sub_concept": data.get("sub_concept"),
        "created_by": data["created_by"],
        "create_date": data.get("create_date", datetime.utcnow()),
        "update_date": data.get("update_date"),
        "complete_date": data.get("complete_date"),
        "status": data.get("status"),
        "questions": data["questions"],
        "score": data.get("score"),
        "answered": data.get("answered"),
        "TestIndicator": data.get("TestIndicator")  # list of strings
    })

    client.put(entity)
    return entity.key




