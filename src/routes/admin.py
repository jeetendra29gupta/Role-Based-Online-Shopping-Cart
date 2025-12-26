from flask import Blueprint
from flask import render_template

from src.utilities.logger import get_logger
from src.utilities.security import login_required
from src.utilities.security import role_required

logger = get_logger(__name__)
admin = Blueprint("admin", __name__)


@admin.route("/dashboard", methods=["GET"])
@login_required
@role_required("admin")
def dashboard():
    return render_template("admin/dashboard.html")
