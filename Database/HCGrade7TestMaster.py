'''
Module:HCGrade7TestMaster

Creates the HCGrade7TestMaster table in GAE.

This tables stores the details of Grade 7 topical tests for each students

Version: 1.0

Created on May 09, 2014

Author:
   Farhat Pachisa (farhat@homecampus.com.sg)
   
Copyright:
    Copyright (c) 2012, Home Campus.  All Rights Reserved.

Usage:
'''

from google.cloud import datastore

client = datastore.Client()

def create_grade7_testmaster(data):
    required_fields = ["test_id", "test_topic", "student_id", "start_date", "test_status", "elapsed_time"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} is required")

    key = client.key("HCGrade7TestMaster")
    entity = datastore.Entity(key=key)

    entity.update({
        "test_id": data["test_id"],
        "test_topic": data["test_topic"],
        "student_id": data["student_id"],
        "start_date": data["start_date"],
        "end_date": data.get("end_date"),
        "test_score": data.get("test_score"),
        "total_marks": data.get("total_marks"),
        "test_status": data["test_status"],
        "elapsed_time": data["elapsed_time"],
        "attempt": data.get("attempt")
    })

    client.put(entity)
    return entity.key




