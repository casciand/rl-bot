import os
import firebase_admin
from firebase_admin import db

creds = firebase_admin.credentials.Certificate(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app(creds, {
    'databaseURL': os.environ.get('DATABASE_URL')
})

users_ref = db.reference("/users")


async def get_user(user_id):
    discord_ids = users_ref.get()

    for id in discord_ids:
        if id == user_id:
            return discord_ids[id]

    return None


async def create_user(user_id, platform, identifier):
    users_ref.child(user_id).set({
        'platform': platform,
        'identifier': identifier
    })
