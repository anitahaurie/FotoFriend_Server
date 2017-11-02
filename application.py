import flask
import os
import boto3
import json

from flask_restful import Resource, Api
from pymongo import MongoClient

application = flask.Flask(__name__)
api = Api(application)

class StoreImage(Resource):
    def post(self):
        username = flask.request.files['username']
        image = flask.request.files['file']

        # Get encrypted username from MongoDB

        #Send "upload" variable to S3 bucket
        s3 = boto3.resource('s3')
        filename = '%s/%s' % (username.stream.read().decode(), image.filename)

        try:
            s3.Bucket('foto-friend').put_object(ACL='public-read', Key=filename, Body=image.stream.read())
        except:
            return 500 # Is this best?

        # Photo URL
        # url = "https://s3-us-west-2.amazonaws.com/foto-friend/" + username + "/" + filename_with_ext
        # Clarifai
        # MongoDB

        return 200

class Login(Resource):
    def post(self):
        data = flask.request.data
        username = json.loads(data)['username']
        print(username)

        #Connect to MongoDB database
        client = MongoClient("mongodb://admin:%s@fotofrienddb-shard-00-00-5xqww.mongodb.net:27017,fotofrienddb-shard-00-01-5xqww.mongodb.net:27017,fotofrienddb-shard-00-02-5xqww.mongodb.net:27017/test?ssl=true&replicaSet=FotoFriendDB-shard-0&authSource=admin" % os.environ['MONGO_PWD'])

        #Check if user already has a collection in the database
        db = client.FotoFriendUserData

        if (not username in db.collection_names()):
           #New user, create new collection for the user
            db.create_collection(username)

            #Create the default keyword with all images
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

api.add_resource(StoreImage, '/storeImage')
api.add_resource(Login, '/login')

#REMINDER: Remove local port 80
if __name__ == '__main__':
    application.debug = False
    application.run()