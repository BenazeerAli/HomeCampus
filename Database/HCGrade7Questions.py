'''
Module:HCGrade7Questions

Creates the HCGrade7Questions table in GAE.

This tables stores the questions and answer details of Grade 7 questions for each students

Version: 1.0

Created on Apr 22, 2014

Author:
   Farhat Pachisa (farhat@homecampus.com.sg)
   
Copyright:
    Copyright (c) 2012, Home Campus.  All Rights Reserved.

Usage:
'''

from google.cloud import datastore

client = datastore.Client()

def create_grade7_question(data):
    required_fields = ["question_id", "question_type", "student_id", "answer_id"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} is required")

    key = client.key("HCGrade7Questions")
    entity = datastore.Entity(key=key)

    entity.update({
        "question_id": data["question_id"],
        "question_type": data["question_type"],
        "student_id": data["student_id"],
        "answer_id": data["answer_id"],
        "entered_answer": data.get("entered_answer"),
        "submitted": data.get("submitted", False),
        "save_date": data.get("save_date"),
        "submit_date": data.get("submit_date"),
        "correct": data.get("correct")
    })

    client.put(entity)
    return entity.key



