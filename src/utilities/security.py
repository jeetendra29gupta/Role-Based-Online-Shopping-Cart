"""
Authentication and authorization utilities.

This module provides:
- Password hashing and verification using bcrypt
- Login-required and role-based access decorators
- Secure session-based access control helpers
"""

from functools import wraps
from typing import Any
from typing import Callable

import bcrypt
from flask import flash
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from src.utilities.config import Config
from src.utilities.logger import get_logger

logger = get_logger(__name__)


def hash_password(plain_password: str) -> str:
    """
    Hash a plain-text password using bcrypt.

    Args:
        plain_password (str): User-provided plain text password.

    Returns:
        str: Bcrypt-hashed password encoded as UTF-8 string.

    Raises:
        ValueError: If the password is empty.
        RuntimeError: If hashing fails.

    Example:
        >>> hashed = hash_password("MySecret123")
        >>> isinstance(hashed, str)
        True
    """
    if not plain_password:
        logger.error("Attempted to hash an empty password")
        raise ValueError("Password must not be empty")

    try:
        salt = bcrypt.gensalt(rounds=Config.SALT_LENGTH)
        hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
        logger.debug("Password hashed successfully")
        return hashed.decode("utf-8")

    except Exception as exc:
        logger.exception("Password hashing failed")
        raise RuntimeError("Failed to hash password") from exc


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a stored bcrypt hash.

    Args:
        plain_password (str): User-provided plain password.
        hashed_password (str): Stored bcrypt hash.

    Returns:
        bool: True if password matches, False otherwise.

    Example:
        >>> verify_password("MySecret123", hashed)
        True
    """
    try:
        is_valid = bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
        logger.debug("Password verification result: %s", is_valid)
        return is_valid

    except Exception:
        logger.exception("Password verification failed")
        return False


def login_required(view: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to enforce authentication on protected routes.

    Redirects unauthenticated users to login page and preserves
    the originally requested URL.

    Args:
        view (Callable): Flask view function.

    Returns:
        Callable: Wrapped view function.

    Example:
        @app.route("/dashboard")
        @login_required
        def dashboard():
            ...
    """

    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            logger.warning(
                "Unauthorized access attempt to %s",
                request.path
            )
            flash("Please log in first", "error")
            return redirect(url_for("user.login", next=request.url))

        logger.debug(
            "User %s accessed %s",
            session.get("user_id"),
            request.path,
        )
        return view(*args, **kwargs)

    return wrapped_view


def role_required(*allowed_roles: str):
    """
    Decorator to restrict access based on user role(s).

    The user's role is expected to be stored in session["role"].

    Args:
        *allowed_roles (str): One or more allowed roles
            (e.g. "admin", "seller", "customer").

    Returns:
        Callable: Wrapped Flask view function.

    Example:
        @app.route("/admin")
        @login_required
        @role_required("admin")
        def admin_panel():
            ...

        @app.route("/inventory")
        @login_required
        @role_required("seller", "admin")
        def inventory():
            ...

        @app.route("/cart")
        @login_required
        @role_required("customer", "seller", "admin")
        def cart():
            ...
    """

    allowed_roles_set = {role.lower() for role in allowed_roles}

    def decorator(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            user_id = session.get("user_id")
            user_role = session.get("role")

            if not user_role:
                logger.warning(
                    "Role missing in session: user_id=%s path=%s",
                    user_id,
                    request.path,
                )
                flash("Access denied", "error")
                return redirect(url_for("index"))

            if user_role.lower() not in allowed_roles_set:
                logger.warning(
                    "Role access denied: user_id=%s role=%s allowed=%s path=%s",
                    user_id,
                    user_role,
                    allowed_roles_set,
                    request.path,
                )
                flash("You do not have permission to access this page", "error")
                return redirect(url_for("index"))

            logger.debug(
                "Role access granted: user_id=%s role=%s path=%s",
                user_id,
                user_role,
                request.path,
            )
            return view(*args, **kwargs)

        return wrapped_view

    return decorator
