import flask
import requests

from flask_restful import Resource, Api

application = flask.Flask(__name__)
api = Api(application)

class Default(Resource):
    def get(self):
        return "Hello, World!"

class StoreImage(Resource):
	def post(self):
		image = flask.request.data

		#Send "upload" variable to S3 bucket


		'''
		if response from S3 bucket is successful
			response = "Your upload was successful!"
			response.status = "200 OK" 
		else
			response = "Something went wrong. Please try again."
			response.status = ???
		'''
		response = 'Your upload was successful!'
		return response, 200

api.add_resource(Default, '/')
api.add_resource(StoreImage, '/storeImage')

#REMINDER: Remove local port 80
if __name__ == '__main__':
    application.debug = False
    application.run()