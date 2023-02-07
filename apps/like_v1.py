from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_refresh_token, jwt_required, create_access_token, get_jwt_identity
from flask_restful import Api, Resource

from constants.http_status_codes import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_200_OK, HTTP_401_UNAUTHORIZED
from models.user_models.models import User, db, Post, Like, Comment, Saved

# from core.domain.account.entity.account import db, User


app = Blueprint('like_api', __name__)

api = Api(app)


@api.resource('/like/<post_id>/')
class LikeResource(Resource):

    @jwt_required()
    def post(self, post_id):
        current_user = get_jwt_identity()

        post = Post.query.filter_by(id=post_id).first()
        like = Like.query.filter_by(
            author=current_user, post_id=post_id).first()

        if not post:
            return jsonify({'error': 'Post does not exists'})
        elif like:
            db.session.delete(like)
            db.session.commit()
            return jsonify({'message': 'You unliked post'})
        else:
            like = Like(author=current_user, post_id=post.id)
            db.session.add(like)
            db.session.commit()

            return jsonify({'message': 'You liked post'})


@api.resource('/bookmarks/<post_id>/')
class BookmarksResource(Resource):

    @jwt_required()
    def post(self, post_id):
        current_user = get_jwt_identity()


        post = Post.query.filter_by(id=post_id).first()
        save = Saved.query.filter_by(post_id=post_id).first()

        if not post:
            return jsonify({'error': 'Post does not exists'})
        elif save:
            db.session.delete(save)
            db.session.commit()
            return jsonify({'message': 'You unsaved post'})

        else:
            save = Saved(author=current_user, post_id=post.id)
            db.session.add(save)
            db.session.commit()
            return jsonify({'message': 'You saved post'})


@api.resource('/bookmarks/')
class BookmarksLiseResource(Resource):

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        # Use the map() function to retrieve the saved posts and filter them by the current user
        saved_posts = map(lambda saved: Post.query.filter_by(
            id=saved.post_id, user_id=current_user).first(),
                          Saved.query.filter_by(author=current_user).all())
        # Use the filter() function to remove any None values
        saved_posts = filter(None, saved_posts)
        # Use the join() method to retrieve the related author information
        saved_posts = Post.query.join(User, Post.user_id == User.id).filter(
            Post.id.in_([post.id for post in saved_posts])).all()
        # Extract the title, body and author of the saved posts
        result = [{"title": post.title, "text": post.body, "author": post.user_id} for post in saved_posts]

        return jsonify(result)