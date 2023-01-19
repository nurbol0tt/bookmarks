from flasgger import swag_from
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import validators
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_refresh_token, jwt_required, create_access_token, get_jwt_identity
from constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from models.user_models.models import User, db

# from core.domain.account.entity.account import db, User


app = Blueprint('account_api', __name__)

api = Api(app)


@api.resource('/register')
class Authorize(Resource):

    def post(self):
        """
        Example endpoint returning a list of colors by palette
        In this example the specification is taken from specs_dict
        """
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']

        if len(username) < 3:
            return jsonify({'error': 'User is too short'}), HTTP_400_BAD_REQUEST

        if not username.isalnum() or " " in username:
            return jsonify({'error': 'Username should be alphanumeric, also no spaces'}), HTTP_400_BAD_REQUEST

        if not validators.email(email):
            return jsonify({'error': 'Email is not valid'}), HTTP_400_BAD_REQUEST

        if len(password) < 3:
            return jsonify({'error': 'Password is too short'}), HTTP_400_BAD_REQUEST

        if User.query.filter_by(email=email).first() is not None:
            print('___________________________________________')

            return jsonify({'error': 'Email is taken'})

        if User.query.filter_by(username=username).first() is not None:
            print('-----------------------------------------------')

            return jsonify({'error': 'Name is taken'})

        pwd_hash = generate_password_hash(password)

        user = User(username=username, password=pwd_hash, email=email)
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'message': "User created",
            'user': {
                'username': username, "email": email
            }

        })


@api.resource('/login')
class Login(Resource):

    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()

        if user:
            is_pass_correct = check_password_hash(user.password, password)

            if is_pass_correct:
                refresh = create_refresh_token(identity=user.id)
                access = create_access_token(identity=user.id)

                return jsonify({
                    'user': {
                        'refresh': refresh,
                        'access': access
                    }
                })

        return jsonify({'error': 'Wrong credentials'})


@api.resource('/me')
class Me(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        user = User.query.filter_by(id=user_id).first()

        return jsonify({
            "username": user.username,
            'email': user.email

        })


@api.resource('/token/refresh')
class Refresh(Resource):

    @jwt_required(refresh=True)
    def get(self):
        identity = get_jwt_identity()
        access = create_access_token(identity=identity)

        return jsonify({
            "access": access
        })
