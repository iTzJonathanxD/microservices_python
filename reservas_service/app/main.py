from flask import Flask
from app.routes.routes import auth_bp, reservas_bp
from app.routes.reporte import reporte_reservas 
from app.database import init_db, db
from app.utils import jwt
from app.config import Config
from strawberry.flask.views import GraphQLView
from app.routes.graphql_routes import schema 
import logging

logging.basicConfig(level=logging.INFO)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)

    with app.app_context():
        try:
            from sqlalchemy import inspect

            inspector = inspect(db.engine)
            if "reservas" not in inspector.get_table_names():
                db.create_all()
                logging.info("Tabla 'reservas' creada exitosamente")
            else:
                logging.info("La tabla 'reservas' ya existe, no se necesita crearla")
        except Exception as e:
            logging.error(f"Error al verificar o crear la tabla 'reservas': {e}")

    app.register_blueprint(auth_bp, url_prefix="/auth") 
    app.register_blueprint(reservas_bp, url_prefix="/api") 
    app.register_blueprint(reporte_reservas)  

    # Registrar GraphQL
    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
    )

    # Inicializar JWT
    jwt.init_app(app)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=8002, debug=True)
