from api.routes.recommendation_system.popularity_bp import popularity_recommend_bp
from api.routes.recommendation_system.collaborative_bp import collaborative_recommend_bp
from api.routes.recommendation_system.hybrid_bp import hybrid_recommend_bp
from api.routes.recommendation_system.main_recommendation_bp import products_recommend_bp
# from routes.chat_vendor_bp import chat_vendor_bp


def app_routes(app):
    app.register_blueprint(popularity_recommend_bp, url_prefix='/api')
    app.register_blueprint(collaborative_recommend_bp, url_prefix='/api')
    app.register_blueprint(hybrid_recommend_bp, url_prefix='/api')
    # app.register_blueprint(products_similarity_bp, url_prefix='/api')

    # app.register_blueprint(products_recommend_bp, url_prefix='/api')
