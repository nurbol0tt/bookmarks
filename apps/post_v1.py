from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
import validators
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user_models.models import db, Post, User, Comment, Like

# from core.domain.account.entity.account import db
# from core.domain.post.entity.post import Post


app = Blueprint('post_api', __name__)

api = Api(app)


@api.resource('/create_post/', methods=['POST'])
class CreatePost(Resource):

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        body = request.get_json().get('body', '')
        title = request.get_json().get('title', '')
        url = request.get_json().get('url', '')

        if not validators.url(url):
            return jsonify({
                'error': 'Enter a valid url'
            })
        post = Post(url=url, body=body, title=title, user_id=current_user)
        db.session.add(post)
        db.session.commit()

        return jsonify({
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "short_url": post.short_url,
            "visits": post.visits,
            "user_id": post.user_id,
            "created_at": post.created_at,
            "updated_at": post.updated_at
        })


@api.resource('/post_list/', methods=['GET'])
class PostList(Resource):

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)

        posts = Post.query.filter_by(
            user_id=current_user).paginate(page=page, per_page=per_page)

        data = []
        user = User.query.filter_by(id=current_user).first()

        for post in posts.items:
            data.append({
                'author': user.username,
                'id': post.id,
                'url': post.url,
                'short_url': post.short_url,
                'visit': post.visits,
                'title': post.title,
                'body': post.body,
                'created_at': post.created_at,
                'updated_at': post.updated_at,
            })

        meta = {
            "page": posts.page,
            'pages': posts.pages,
            'total_count': posts.total,
            'prev_page': posts.prev_num,
            'next_page': posts.next_num,
            'has_next': posts.has_next,
            'has_prev': posts.has_prev,

        }

        return jsonify({'data': data, "meta": meta})


@api.resource('/post_detail/<int:pk>/', methods=['GET'])
class PostDetail(Resource):

    @jwt_required()
    def get(self, pk):
        current_user = get_jwt_identity()

        post = Post.query.filter_by(id=pk).first()
        comment = Comment.query.filter_by(post_id=pk).all()
        like = Like.query.filter_by(post_id=pk).all()

        result_comment = []
        for ct in comment:
            result_comment.append({'author': ct.author, 'text': ct.text})

        if not post:
            return jsonify({
                "message": "Item not found"
            })

        return jsonify({
            'id': post.id,
            'url': post.url,
            'short_url': post.short_url,
            'visit': post.visits,
            'title': post.title,
            'body': post.body,
            'created_at': post.created_at,
            'updated_at': post.updated_at,

            "comment": result_comment,
            "like": len(like)

        })


@api.resource('/post_update/<int:pk>/')
class PostUpdate(Resource):

    @jwt_required()
    def put(self, pk):
        current_user = get_jwt_identity()

        post = Post.query.filter_by(user_id=current_user, id=pk).first()

        if not post:
            return jsonify({'message': 'Item not found'})

        body = request.get_json().get('body', '')
        title = request.get_json().get('title', '')
        url = request.get_json().get('url', '')

        if not validators.url(url):
            return jsonify({
                'error': 'Enter a valid url'
            })

        post.url = url
        post.title = title
        post.body = body

        db.session.commit()

        return jsonify({
            'id': post.id,
            'url': post.url,
            'short_url': post.short_url,
            'visit': post.visits,
            'title': post.title,
            'body': post.body,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
        })


@api.resource('/post_delete/<int:pk>/')
class PostDelete(Resource):

    @jwt_required()
    def delete(self, pk):
        post = Post.query.filter_by(id=pk).first()

        if not post:
            return jsonify({'message': 'Item not found'})

        db.session.delete(post)
        db.session.commit()

        return jsonify({})
