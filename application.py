import flask
import os
import boto3
import json

from flask_restful import Resource, Api
from pymongo import MongoClient
from clarifai.rest import ClarifaiApp

application = flask.Flask(__name__)
api = Api(application)

def inc(x):
    return x + 1

def create_app():
    return application

class Ping(Resource):
    def get(self):
        return flask.jsonify(ping='pong')

class StoreImage(Resource):
    def post(self):
        username = flask.request.files['username']
        image = flask.request.files['file']

        # Get encrypted username from MongoDB
        # Connect to MongoDB database
        client = MongoClient("mongodb://admin:%s@fotofrienddb-shard-00-00-5xqww.mongodb.net:27017,fotofrienddb-shard-00-01-5xqww.mongodb.net:27017,fotofrienddb-shard-00-02-5xqww.mongodb.net:27017/test?ssl=true&replicaSet=FotoFriendDB-shard-0&authSource=admin" % os.environ['MONGO_PWD'])

        # Get user collection
        db = client.FotoFriendUserData
        userCollection = db.get_collection(username.stream.read().decode())
        document = userCollection.find_one({"Concept":{"$eq":"Default"}})
        encryptUsername = document['_id']

        # Send "upload" variable to S3 bucket
        s3 = boto3.resource('s3')
        filename = '%s/%s' % (encryptUsername, image.filename)

        try:
            s3.Bucket('foto-friend').put_object(ACL='public-read', Key=filename, Body=image.stream.read())
        except:
            return 500 # Is this best?

        # Photo URL
        imageURL = "https://s3-us-west-2.amazonaws.com/foto-friend/" + filename

        # Clarifai
        app = ClarifaiApp()
        model = app.models.get('general-v1.3')
        response = model.predict_by_url(url = imageURL)

        # MongoDB
        concepts = response['outputs'][0]['data']['concepts']
        for concept in concepts:
            if concept['value'] > 0.90:
                userCollection.update(
                    {'Concept': concept['name']},
                    {"$addToSet": {"Links": imageURL}},
                    upsert = True)

        # Add link to default
        userCollection.update(
            {'Concept': "Default"},
            {"$addToSet": {"Links": imageURL}},
            upsert = True)

        return 200

class Login(Resource):
    def post(self):
        data = flask.request.data.decode('utf-8')
        username = json.loads(data)['username']

        # Connect to MongoDB database
        client = MongoClient("mongodb://admin:%s@fotofrienddb-shard-00-00-5xqww.mongodb.net:27017,fotofrienddb-shard-00-01-5xqww.mongodb.net:27017,fotofrienddb-shard-00-02-5xqww.mongodb.net:27017/test?ssl=true&replicaSet=FotoFriendDB-shard-0&authSource=admin" % os.environ['MONGO_PWD'])

        # Check if user already has a collection in the database
        db = client.FotoFriendUserData

        if (not username in db.collection_names()):
           # New user, create new collection for the user
            db.create_collection(username)

            # Create the default keyword with all images
            db.get_collection(username).update(
            {'Concept': "Default"}, 
            {"$addToSet": {"Links": ""}},
            upsert = True)

        userCollection = db.get_collection(username)

        document = userCollection.find_one({"Concept":{"$eq":"Default"}})

        links = document['Links']

        response = flask.make_response(json.dumps({'Links' : links}))
        response.headers['Content-type'] = 'application/json'

        return response

class Filter(Resource):
    def post(self):
        data = flask.request.data.decode('utf-8')
        username = json.loads(data)['username']
        keywords = json.loads(data)['keywords']

        # Connect to MongoDB database
        client = MongoClient("mongodb://admin:%s@fotofrienddb-shard-00-00-5xqww.mongodb.net:27017,fotofrienddb-shard-00-01-5xqww.mongodb.net:27017,fotofrienddb-shard-00-02-5xqww.mongodb.net:27017/test?ssl=true&replicaSet=FotoFriendDB-shard-0&authSource=admin" % os.environ['MONGO_PWD'])

        # Check if user already has a collection in the database
        db = client.FotoFriendUserData
        userCollection = db.get_collection(username)
        document = userCollection.find_one({"Concept":{"$eq":"Default"}})
        links = set(document['Links'])

        for keyword in keywords:
            document = userCollection.find_one({"Concept":{"$eq":keyword}})
            if document == None:
                links.clear()
                break
            else:
                links = links & set(document['Links'])

        response = flask.make_response(json.dumps({'Links' : list(links)}))
        response.headers['Content-type'] = 'application/json'
        return response

class DeleteImage(Resource):
    def post(self):
        data = flask.request.data.decode('utf-8')
        username = json.loads(data)['username']
        url = json.loads(data)['url']

        # Get encrypted username from MongoDB
        # Connect to MongoDB database
        client = MongoClient("mongodb://admin:%s@fotofrienddb-shard-00-00-5xqww.mongodb.net:27017,fotofrienddb-shard-00-01-5xqww.mongodb.net:27017,fotofrienddb-shard-00-02-5xqww.mongodb.net:27017/test?ssl=true&replicaSet=FotoFriendDB-shard-0&authSource=admin" % os.environ['MONGO_PWD'])

        # Get user collection
        db = client.FotoFriendUserData
        userCollection = db.get_collection(username)
        document = userCollection.find_one({"Concept":{"$eq":"Default"}})
        encryptUsername = document['_id']

        # Remove variable from S3 bucket
        s3 = boto3.resource('s3')
        url_split = url.split('/')
        filename = '%s/%s' % (url_split[4], url_split[5])

        try:
            s3.Bucket('foto-friend').delete_objects(Delete={ 'Objects': [ {'Key': filename} ] })
        except:
            return 500 # Is this best?

        # Update MongoDB to not include URL
        userCollection.update(
            {},
            { '$pull': { 'Links': url }},
            upsert = False,
            multi = True
        )

        return 200

api.add_resource(StoreImage, '/storeImage')
api.add_resource(Login, '/login')
api.add_resource(Filter, '/filter')
api.add_resource(DeleteImage, '/deleteImage')
api.add_resource(Ping, '/ping')

#REMINDER: Remove local port 80
if __name__ == '__main__':
    application.debug = False
    application.run()