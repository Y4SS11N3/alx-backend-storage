#!/usr/bin/env python3
"""Module for inserting a new document in a collection"""


def insert_school(mongo_collection, **kwargs):
    """
    Inserts a new document in a collection based on kwargs
    Returns the new _id
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
