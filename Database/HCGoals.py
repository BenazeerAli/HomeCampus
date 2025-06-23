'''
Module:HCGoals

Creates the HCGoals table in GAE.

This tables stores all the goals information for a student.

Version: 1.0

Created on Oct 08, 2012

Author:
   Farhat Pachisa (farhat@homecampus.com.sg)
   
Copyright:
    Copyright (c) 2012, Home Campus.  All Rights Reserved.

Usage:
'''

from google.cloud import datastore

client = datastore.Client()

def create_hcgoals_entity(data):
    if "student_id" not in data:
        raise ValueError("student_id is required")

    key = client.key("HCGoals")
    entity = datastore.Entity(key=key)

    entity.update({
        "student_id": data["student_id"],
        "grade": data.get("grade"),
        "topic": data.get("topic"),
        "subTopic": data.get("subTopic"),
        "goalName": data.get("goalName"),
        "target": data.get("target"),
        "created_by": data.get("created_by"),
        "create_date": data.get("create_date"),
        "update_date": data.get("update_date"),
        "update_by": data.get("update_by"),
        "complete_date": data.get("complete_date"),
        "status": data.get("status")
    })

    client.put(entity)
    return entity.key





