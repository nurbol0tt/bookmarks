from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_refresh_token, jwt_required, create_access_token, get_jwt_identity
from flask_restful import Api, Resource

from constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from models.user_models.models import User, db, Post, Like, Comment

# from core.domain.account.entity.account import db, User


app = Blueprint('comment_api', __name__)

api = Api(app)


@api.resource('/create_comment/<post_id>/')
class CommentResource(Resource):

    @jwt_required()
    def post(self, post_id):
        current_user = get_jwt_identity()
        text = request.get_json().get('text', '')

        if not text:
            return jsonify({'messages': 'Comment cannot be empty'})
        else:
            post = Post.query.filter_by(id=post_id)
            if post:
                comment = Comment(
                    text=text, author=current_user, post_id=post_id
                )
                db.session.add(comment)
                db.session.commit()
            else:
                return jsonify({'messages': 'Post does not exists'})
        return jsonify({'messages': 'created', 'text': text})


@api.resource('/comment_update/<int:pk>/')
class CommentUpdateResource(Resource):

    @jwt_required()
    def put(self, pk):
        current_user = get_jwt_identity()

        comment = Comment.query.filter_by(id=pk).first()

        text = request.get_json().get('text', '')

        if not comment:
            return jsonify({'messages': 'Comment cannot be empty'})
        elif current_user.id != comment.author and current_user.id != comment.post.author:
            return jsonify({'messages': 'You do not have permission to delete this comment.'})
        else:
            comment.text = text
            db.session.commit()
        return jsonify({'messages': text})


@api.resource('/comment_delete/<int:pk>/')
class CommentDeleteResource(Resource):

    @jwt_required()
    def delete(self, pk):
        current_user = get_jwt_identity()

        comment = Comment.query.filter_by(id=pk).first()
        print(comment)

        if not comment:
            return jsonify({'messages': 'Comment does not exists'})
        elif current_user != comment.author and current_user != comment.post.author:
            return jsonify({'messages': 'You do not have permission to delete this comment.'})
        else:
            print('DELETE')
            db.session.delete(comment)
            db.session.commit()

        return jsonify({})
