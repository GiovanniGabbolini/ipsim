"""
Created on Mon Mar 02 2020

@author Giovanni Gabbolini
"""


from src.mongo.Mongo import Mongo
from beeprint import pp
import pymongo
from src.utils import menu


def feature_outcome_statistics(how_many_documents=-1, db='log_feature'):
    db = Mongo.getInstance()[db]
    names = [collection for collection in db.list_collection_names()
             if not collection.startswith('system.')]
    stats_dict = {}

    for collection_name in names:
        c = db[collection_name]
        start_date = None
        end_date = None
        count_true = 0
        # for idx, d in enumerate(c.find().sort([("timestamp", pymongo.DESCENDING)])):
        for idx, d in enumerate(c.find().sort([("_id", pymongo.DESCENDING)])):
            if idx == 0:
                start_date = d['timestamp']

            count_true += 1 if d['outcome'] == True else 0

            if idx == how_many_documents - 1:
                break

        stats_dict[collection_name] = {
            'name': collection_name,
            'number positive outcomes': count_true,
            'perc positive outcomes': count_true/idx,
            'start date': start_date.strftime("%Y-%m-%d %H:%M"),
            'end date': d['timestamp'].strftime("%Y-%m-%d %H:%M"),
        }

    for key in stats_dict.keys():
        pp(stats_dict[key])


if __name__ == "__main__":
    choice = menu.single_choice('Pick one', ['Stats features', 'Stats segue'])
    if choice == 'Stats features':
        feature_outcome_statistics(how_many_documents=500, db='log_feature')
    if choice == 'Stats segue':
        feature_outcome_statistics(how_many_documents=500, db='log_segue')
