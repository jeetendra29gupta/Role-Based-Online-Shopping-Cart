from flask import Flask

from src.routes.admin import admin
from src.routes.auth import auth
from src.routes.customer import customer
from src.routes.seller import seller
from src.routes.user import user
from src.utilities.config import Config
from src.utilities.database import init_table
from src.utilities.logger import get_logger

logger = get_logger(__name__)
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

host = Config.HOST
port = Config.PORT
debug = Config.DEBUG

app.register_blueprint(user, url_prefix="")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(seller, url_prefix="/seller")
app.register_blueprint(customer, url_prefix="/customer")

if __name__ == '__main__':
    logger.info("Application is starting")
    with app.app_context():
        logger.info("Initializing database")
        init_table()
    logger.info(f"Application started on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
