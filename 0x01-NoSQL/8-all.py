#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module defines list_all function.

Example:
    schools = list_all(school_collection)

"""


def list_all(mongo_collection):
    """List all documents in a collection.

    Args:
        mongo_collection (object): pymongo collection object.

    Returns:
        list.
    """
    return mongo_collection.find()
