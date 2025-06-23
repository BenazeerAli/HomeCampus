'''
Module:TestProblems

Creates the test problems table in GAE.

This tables stores all the problem information of the test.

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

def create_test_problem(data):
    required_fields = ["test_id", "concept", "counter", "problem_type"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} is required")

    key = client.key("TestProblems")
    entity = datastore.Entity(key=key)

    entity.update({
        "test_id": data["test_id"],
        "concept": data["concept"],
        "counter": data["counter"],
        "problem_type": data["problem_type"],
        "problem": data.get("problem"),
        "dollar_unit": data.get("dollar_unit"),
        "unit": data.get("unit"),
        "answer": data.get("answer"),
        "answer_submitted": data.get("answer_submitted"),
        "correct": data.get("correct"),
        "time_taken": data.get("time_taken"),
        "submit_date": data.get("submit_date", datetime.utcnow()),
        "complexity_level": data.get("complexity_level"),
        "template": data.get("template"),
        "answer1": data.get("answer1"),
        "answer2": data.get("answer2"),
        "answer3": data.get("answer3"),
        "answer4": data.get("answer4"),
        "answerM1": data.get("answerM1"),
        "answerM2": data.get("answerM2"),
        "answerM3": data.get("answerM3"),
        "answerM4": data.get("answerM4"),
        "answerN1": data.get("answerN1"),
        "answerN2": data.get("answerN2"),
        "answerN3": data.get("answerN3"),
        "answerN4": data.get("answerN4"),
        "answerD1": data.get("answerD1"),
        "answerD2": data.get("answerD2"),
        "answerD3": data.get("answerD3"),
        "answerD4": data.get("answerD4"),
        "value1": data.get("value1"),
        "value2": data.get("value2"),
        "value3": data.get("value3"),
        "value4": data.get("value4"),
        "explain": data.get("explain"),
        "CheckAnswerType": data.get("CheckAnswerType"),
        "status": data.get("status"),
        "FunctionCall": data.get("FunctionCall"),
        "FractionAnswer": data.get("FractionAnswer")
    })

    client.put(entity)
    return entity.key
