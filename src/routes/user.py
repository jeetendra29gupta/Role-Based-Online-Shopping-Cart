from flask import Blueprint
from flask import render_template
from flask import request
from sqlmodel import Session
from sqlmodel import select

from src.models.inventory import Inventory
from src.utilities.database import engine
from src.utilities.logger import get_logger

logger = get_logger(__name__)
user = Blueprint("user", __name__)


@user.route('/')
def index():
    page = int(request.args.get("page", 1))
    per_page = 8
    offset = (page - 1) * per_page

    with Session(engine) as db_session:
        inventories = db_session.exec(
            select(Inventory)
            .where(Inventory.is_active == True)  # noqa
            .offset(offset)
            .limit(per_page)
        ).all()
    return render_template('index.html', inventories=inventories, page=page)
