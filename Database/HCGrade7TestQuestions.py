'''
Module:HCGrade7TestQuestions

Creates the HCGrade7TestQuestions table in GAE.

This tables stores the questions and answer details of Grade 7 Topical test questions for each students

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

def create_grade7_test_question(data):
    required_fields = ["test_id", "question_id", "student_id", "answer_id"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} is required")

    key = client.key("HCGrade7TestQuestions")
    entity = datastore.Entity(key=key)

    entity.update({
        "test_id": data["test_id"],
        "question_id": data["question_id"],
        "student_id": data["student_id"],
        "answer_id": data["answer_id"],
        "entered_answer": data.get("entered_answer"),
        "correct": data.get("correct"),
        "question_marks": data.get("question_marks"),
        "scored_marks": data.get("scored_marks")
    })

    client.put(entity)
    return entity.key




