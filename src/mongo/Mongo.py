"""
Created on Tue Feb 25 2020

@author Giovanni Gabbolini
"""
from pymongo import MongoClient


class Mongo:
    __instance = None

    @staticmethod
    def getInstance():
        if Mongo.__instance == None:
            Mongo.__instance = MongoClient('localhost', 27017, username="giovanni", password="chiara")
        return Mongo.__instance
