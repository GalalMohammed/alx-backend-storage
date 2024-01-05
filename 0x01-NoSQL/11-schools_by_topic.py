#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module defines schools_by_topic function.

Example:
    schools = schools_by_topic(school_collection, "Python")

"""


def schools_by_topic(mongo_collection, topic):
    """Get the list of school having a specific topic.

    Args:
        mongo_collection (object): pymongo collection object.
        topic (str): topic will be searched.

    Returns:
        list.

    """
    return mongo_collection.find({"topics": topic})
