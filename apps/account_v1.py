from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource
import validators
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_refresh_token, jwt_required, create_access_token, get_jwt_identity


from apps.utils import send_reset_email
from constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from models.user_models.models import User, db, Post

app = Blueprint('account_api', __name__)

api = Api(app)
bcrypt = Bcrypt()


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

            return jsonify({'error': 'Email is taken'})

        if User.query.filter_by(username=username).first() is not None:

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

        if user and bcrypt.check_password_hash(user.password, password):

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
        posts = Post.query.filter_by(user_id=user_id).all()
        result = [{"title": post.title, "text": post.body, "author": post.user_id} for post in posts]

        return jsonify({
            "username": user.username,
            'email': user.email,
            'post': result
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


@api.resource("/reset_password/")
class ResetResource(Resource):

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        user = User.query.filter_by(id=user_id).first()
        user = User.query.filter_by(email=user.email).first()
        send_reset_email(user)

        return jsonify({
            'messages': 'An email has been sent with instructions to reset your password'
        })


@api.resource("/reset_password/<token>/")
class ResetTokenResource(Resource):

    def post(self, token):
        user = User.verify_reset_token(token)
        data = request.get_json()
        password = data['password']
        if user is None:
            return jsonify({
                "messages": "That is an invalid or expired token"
            })
        print(password)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        print(hashed_password)
        user.password = hashed_password

        db.session.commit()
        print(user.password)
        return jsonify({
            "messages": "Your password has been updated! You are now able to log in"
        })
