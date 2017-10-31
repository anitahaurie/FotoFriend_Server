import flask
from flask_restful import Resource, Api
import boto3

application = flask.Flask(__name__)
api = Api(application)

class Default(Resource):
    def get(self):
        return "Hello, World!"

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

api.add_resource(Default, '/')
api.add_resource(StoreImage, '/storeImage')

#REMINDER: Remove local port 80
if __name__ == '__main__':
    application.debug = False
    application.run()