import flask

from flask_restful import Resource, Api

application = flask.Flask(__name__)
api = Api(application)

class Default(Resource):
    def get(self):
        return "Hello, World!"

api.add_resource(Default, '/')

if __name__ == '__main__':
    application.debug = False
    application.run()