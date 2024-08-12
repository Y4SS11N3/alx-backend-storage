#!/usr/bin/env python3
"""Module for listing all documents in a collection"""


def list_all(mongo_collection):
    """
    Lists all documents in a collection
    Returns an empty list if no document in the collection
    """
    return list(mongo_collection.find())
