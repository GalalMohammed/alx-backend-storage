#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module defines update_topics function.

Example:
    update_topics(collection, "Holberton school", ["Sys admin", "Algorithm"])

"""


def update_topics(mongo_collection, name, topics):
    """Change all topics of a school document based on the name.

    Args:
        mongo_collection (object): pymongo collection object.
        name (string): the school name to update.
        topics (list): the list of topics approached in the school.

    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
