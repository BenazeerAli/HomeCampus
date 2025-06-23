'''
Module:HCSchoolInfo

Creates the school info table in GAE.

This tables stores all the master information of the schools registered with HC.

Version: 1.0

Created on Sep 03, 2013

Author:
   Farhat Pachisa (farhat@homecampus.com.sg)
   
Copyright:
    Copyright (c) 2012, Home Campus.  All Rights Reserved.

Usage:
'''

from google.cloud import datastore

client = datastore.Client()

def create_school_info_entity(data):
    key = client.key("HCSchoolInfo")
    entity = datastore.Entity(key=key)

    entity.update({
        "teacher_username": data.get("teacher_username"),
        "school_name": data.get("school_name"),
        "school_city": data.get("school_city"),
        "school_country": data.get("school_country")
    })

    client.put(entity)
    return entity.key




