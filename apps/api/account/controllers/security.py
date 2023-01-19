from flask import Blueprint
from flask_restful import Resource


api = Blueprint('api', __name__)


@api.route('/authorize')
class Authorize(Resource):
    def get(self):
        return ['authorize']


@api.route('/logout')
class Logout(Resource):
    def get(self):
        return {'logout': True}


@api.route('/inquiry')
class Inquiry(Resource):
    def get(self):
        return ['Query']


@api.route('/token')
class Token(Resource):
    @api.doc('Exchange Tokens')
    def get(self):
        return ['Token']
