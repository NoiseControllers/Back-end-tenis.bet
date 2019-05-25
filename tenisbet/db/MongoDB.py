import pymongo


class MongoDB(object):
    _client = pymongo.MongoClient("localhost", 27017)
    db = _client["tenisbet"]
