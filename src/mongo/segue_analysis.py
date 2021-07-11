"""
Created on Mon Mar 02 2020

@author Giovanni Gabbolini
"""


from src.mongo.Mongo import Mongo
import pymongo


def segue_analysis(collection_name='semantical_association', how_many_documents=100):
    db = Mongo.getInstance()['log_segue']
    c = db[collection_name]
    start_date = None
    end_date = None
    for idx, d in enumerate(c.find().sort([("timestamp", pymongo.DESCENDING)])):
        if idx == 0:
            start_date = d.timestamp

        # do stats here

        if idx == how_many_documents - 1:
            end_date = d.timestamp
            break


if __name__ == "__main__":
    segue_analysis()
