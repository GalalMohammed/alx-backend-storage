#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module defines inser_school function.
Example:
    id = insert_school(collection, name="UCSF", address="505 Parnassus Ave")

"""


def insert_school(mongo_collection, **kwargs):
    """insert a new document in a collection based on kwargs.

    Args:
        mongo_collection (object): pymongo collection object.
        **kwargs: mew object attrs.

    Returns:
        the new _id.
    """
    return mongo_collection.insert_one(kwargs).inserted_id
