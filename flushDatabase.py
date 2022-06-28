# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 09:21:54 2022

@author: Ismail
"""
# Delete all documents in a db

import pymongo

client = pymongo.MongoClient()
db = client["database"]
db.transactions.delete_many({});