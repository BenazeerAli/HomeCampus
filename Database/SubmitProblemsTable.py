'''
Module:CreateProblemsTable

Creates the problems table in sqlite3.

This tables stores all the information when student submits the answer to a problem.

Created on Jan 13, 2011

@author: Farhat
'''


from google.cloud import datastore
from datetime import datetime

client = datastore.Client()

def create_problems_table_entity(data):
    required_fields = ["student_id", "grade", "concept"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"{field} is required")

    key = client.key("ProblemsTable")
    entity = datastore.Entity(key=key)

    entity.update({
        "student_id": data["student_id"],
        "grade": data["grade"],
        "concept": data["concept"],
        "problem": data.get("problem"),
        "problem_type": data.get("problem_type"),
        "answer": data.get("answer"),
        "MCQ": data.get("MCQ"),
        "correct": data.get("correct"),
        "answer_submitted": data.get("answer_submitted"),
        "time_taken": data.get("time_taken"),
        "MCQAnswers": data.get("MCQAnswers"),
        "submit_date": data.get("submit_date", datetime.utcnow()),
        "complexity_level": data.get("complexity_level"),
        "HCScore": data.get("HCScore"),
        "dollar_unit": data.get("dollar_unit"),
        "unit": data.get("unit"),
        "template": data.get("template"),
        "explain": data.get("explain"),
        "FunctionCall": data.get("FunctionCall"),
        "FractionAnswer": data.get("FractionAnswer"),
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
        "CheckAnswerType": data.get("CheckAnswerType")
    })

    client.put(entity)
    return entity.key




