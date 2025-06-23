'''
Module:HCStudents

Creates the HCStudents table in GAE.

This tables stores the students--class information.

Version: 1.0

Created on Sep 10, 2013

Author:
   Farhat Pachisa (farhat@homecampus.com.sg)
   
Copyright:
    Copyright (c) 2012, Home Campus.  All Rights Reserved.

Usage:
'''

from google.cloud import datastore
from datetime import datetime

client = datastore.Client()

def create_hc_student(data):
    key = client.key("HCStudents")
    entity = datastore.Entity(key=key)

    entity.update({
        "teacher_username": data.get("teacher_username"),
        "class_name": data.get("class_name"),
        "student_first_name": data.get("student_first_name"),
        "student_last_name": data.get("student_last_name"),
        "student_username": data.get("student_username"),
        "join_date": datetime.utcnow(),
        "student_rollno": data.get("student_rollno")
    })

    client.put(entity)
    return entity.key

