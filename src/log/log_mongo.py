"""
Created on Tue Feb 25 2020

@author Giovanni Gabbolini
"""


from src.mongo.Mongo import Mongo


def log_mongo(name, to_save, db_name='log_segue'):
    """save in a mongo collection

    Arguments:
        name {string} -- name of the collection
        to_save {obj} -- object to save. it must be either dict or list (of dicts)
    """
    coll = Mongo.getInstance()[db_name][name]
    if type(to_save) == dict:
        coll.insert_one(to_save)
    if type(to_save) == list:
        coll.insert_many(to_save)
