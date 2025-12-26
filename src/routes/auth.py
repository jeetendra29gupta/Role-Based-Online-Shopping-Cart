from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from sqlmodel import Session
from sqlmodel import select

from src.models.user import User
from src.models.user import UserRole
from src.utilities.database import engine
from src.utilities.logger import get_logger
from src.utilities.security import hash_password
from src.utilities.security import login_required
from src.utilities.security import verify_password

logger = get_logger(__name__)
auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("auth/signup.html")

    full_name = request.form.get("full_name").strip()
    if not full_name:
        message = "Full name is required"
        flash(message, "Error")
        logger.error(message)
        return redirect(url_for("auth.signup"))

    email_id = request.form.get("email_id").strip()
    if not email_id:
        message = "Email ID is required"
        flash(message, "Error")
        logger.error(message)
        return redirect(url_for("auth.signup"))

    password = request.form.get("password").strip()
    if not password:
        message = "Password is required"
        flash(message, "Error")
        logger.error(message)
        return redirect(url_for("auth.signup"))

    phone_no = request.form.get("phone_no").strip()

    with Session(engine) as db_session:
        db_user = db_session.exec(
            select(User).where(User.email_id == email_id)
        ).one_or_none()
        if db_user:
            message = "Email ID already exists"
            flash(message, "Error")
            return redirect(url_for("auth.signup"))

        hashed_password = hash_password(password)
        new_user = User(
            full_name=full_name,
            email_id=email_id,
            hashed_password=hashed_password,
            phone_no=phone_no,
            role=UserRole.CUSTOMER,
        )
        try:
            db_session.add(new_user)
            db_session.commit()
            db_session.refresh(new_user)

            message = f"User created successfully {new_user.full_name}"
            flash(message, "Success")
            logger.info(message)


        except Exception as e:
            logger.exception(str(e))
            flash(str(e), "Error")

    return redirect(url_for("auth.login"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")

    email_id = request.form.get("email_id").strip()
    if not email_id:
        message = "Email ID is required"
        flash(message, "Error")
        logger.error(message)
        return redirect(url_for("auth.login"))

    password = request.form.get("password").strip()
    if not password:
        message = "Password is required"
        flash(message, "Error")
        logger.error(message)
        return redirect(url_for("auth.login"))

    with Session(engine) as db_session:
        try:
            db_user = db_session.exec(
                select(User).where(User.email_id == email_id, User.is_active == True)  # noqa
            ).one_or_none()
            if not db_user:
                message = "Invalid email id"
                flash(message, "Error")
                logger.error(message)
                return redirect(url_for("auth.login"))

            if not verify_password(password, db_user.hashed_password):
                message = "Invalid password"
                flash(message, "Error")
                logger.error(message)
                return redirect(url_for("auth.login"))

            session["user_id"] = db_user.id
            session["full_name"] = db_user.full_name
            session["role"] = db_user.role

            if db_user.role == UserRole.ADMIN:
                message = f"Admin logged in successfully: {db_user.full_name}"
                flash(message, "Success")
                logger.info(message)

            elif db_user.role == UserRole.SELLER:
                message = f"Seller logged in successfully: {db_user.full_name}"
                flash(message, "Success")
                logger.info(message)

            elif db_user.role == UserRole.CUSTOMER:
                message = f"Customer logged in successfully: {db_user.full_name}"
                flash(message, "Success")
                logger.info(message)

            else:
                message = f"Invalid role for user: {db_user.full_name}"
                flash(message, "Error")
                logger.error(message)

            return redirect(url_for("user.index"))

        except Exception as e:
            logger.exception(str(e))
            flash(str(e), "Error")
            return redirect(url_for("auth.login"))


@auth.route("/logout")
@login_required
def logout():
    session.clear()
    logger.info(f"User logged out successfully: {session.get('full_name')}")
    flash("You have been logged out", "Success")
    return redirect(url_for("user.index"))
