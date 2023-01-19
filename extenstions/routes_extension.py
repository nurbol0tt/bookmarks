from apps.account_v1 import app as account_api
from apps.post_v1 import app as post_api


def register_routes(app):
    """
    Register routes with blueprint and namespace
    """
    app.register_blueprint(account_api)
    app.register_blueprint(post_api)
