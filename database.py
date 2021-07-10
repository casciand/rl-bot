from pymongo import MongoClient


def initiate_cluster(CONNECTION_URL):
    cluster = MongoClient(CONNECTION_URL)

    db = cluster['vgadiscord']
    collection = db['userinfo']

    return collection


def create_user(collection, user_id, platform, identifier):
    user = {'_id': user_id,
            'platform': platform,
            'identifier': identifier}

    collection.insert_one(user)
