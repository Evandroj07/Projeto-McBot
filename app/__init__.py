from flask import Flask
from config import Config
from app.extensions import db, bcrypt, jwt
from app.routes.main import main_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializa extensões com o app
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Importa e registra os Blueprints (Rotas)
    from app.routes.auth import auth_bp
    from app.routes.dados import dados_bp
    # from app.routes.main import main_bp (se tiver criado)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dados_bp)
    app.register_blueprint(main_bp)

    # Cria as tabelas e garante os roles (Seed)
    with app.app_context():
        # Importar modelos para o SQLAlchemy reconhecê-los antes do create_all
        from app.models import Usuario, Funcao, DadoProcessado 
        
        db.create_all()
        
        # Seeding inicial
        if not Funcao.query.filter_by(nome_funcao='Admin').first():
            db.session.add(Funcao(nome_funcao='Admin'))
        if not Funcao.query.filter_by(nome_funcao='User').first():
            db.session.add(Funcao(nome_funcao='User'))
        db.session.commit()

    return app