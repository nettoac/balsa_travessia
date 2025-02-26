from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Carrega as configurações

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.balsa_routes import balsa_bp
    from .routes.veiculo_routes import veiculo_bp
    from .routes.viagem_routes import viagem_bp
    from .routes.registro_routes import registro_bp
    from .routes.relatorio_routes import relatorio_bp
    from .routes import main_bp

    app.register_blueprint(balsa_bp)
    app.register_blueprint(veiculo_bp)
    app.register_blueprint(viagem_bp)
    app.register_blueprint(registro_bp)
    app.register_blueprint(relatorio_bp)
    app.register_blueprint(main_bp)

    return app