import os
import re
from math import ceil

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from sqlmodel import Session
from sqlmodel import or_
from sqlmodel import select

from src.models.inventory import Inventory
from src.utilities.database import engine
from src.utilities.helper import get_utc_now
from src.utilities.logger import get_logger
from src.utilities.security import login_required
from src.utilities.security import role_required

logger = get_logger(__name__)
seller = Blueprint("seller", __name__)
UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ITEMS_PER_PAGE = 10


@seller.route("/dashboard", methods=["GET"])
@login_required
@role_required("seller", "admin")
def dashboard():
    seller_id = session.get("user_id")
    query = request.args.get("q", "").strip()
    sort = request.args.get("sort", "")
    page = request.args.get("page", 1, type=int)

    with Session(engine) as db_session:
        stmt = select(Inventory).where(
            Inventory.seller_id == seller_id,
            Inventory.is_active == True
        )

        if query:
            stmt = stmt.where(
                or_(
                    Inventory.name.ilike(f"%{query}%"),
                    Inventory.description.ilike(f"%{query}%")
                )
            )

        total_items = len(db_session.exec(stmt).all())
        total_pages = ceil(total_items / ITEMS_PER_PAGE)

        if sort == "name_asc":
            stmt = stmt.order_by(Inventory.name.asc())
        elif sort == "name_desc":
            stmt = stmt.order_by(Inventory.name.desc())
        elif sort == "price_asc":
            stmt = stmt.order_by(Inventory.price.asc())
        elif sort == "price_desc":
            stmt = stmt.order_by(Inventory.price.desc())
        elif sort == "date_asc":
            stmt = stmt.order_by(Inventory.created_at.asc())
        elif sort == "date_desc":
            stmt = stmt.order_by(Inventory.created_at.desc())
        else:
            stmt = stmt.order_by(Inventory.created_at.desc())

        stmt = stmt.offset((page - 1) * ITEMS_PER_PAGE).limit(ITEMS_PER_PAGE)
        inventories = db_session.exec(stmt).all()
    return render_template("seller/dashboard.html",
                           inventories=inventories, total_pages=total_pages, page=page, search_query=query, sort=sort)


@seller.route("/add-inventory", methods=["GET", "POST"])
@login_required
@role_required("seller")
def add_inventory():
    if request.method == "GET":
        return render_template("seller/add-inventory.html")

    name = request.form.get("name").strip()
    description = request.form.get("description").strip()
    if not name or not description:
        message = "Name and description are required"
        flash(message, "Error")
        logger.error(message)
        return redirect(url_for("seller.add_inventory"))

    price = request.form.get("price").strip()
    if not price:
        message = "Price is required"
        flash(message, "Error")
        logger.error(message)
        return redirect(url_for("seller.add_inventory"))

    try:
        price = float(price)
        if price <= 0:
            raise ValueError
    except ValueError:
        message = "Price must be a positive number"
        flash(message, "Error")
        logger.error(message)
        return redirect(url_for("seller.add_inventory"))

    quantity = request.form.get("quantity").strip()
    if not quantity:
        message = "Quantity is required"
        flash(message, "Error")
        logger.error(message)
        return redirect(url_for("seller.add_inventory"))

    try:
        quantity = int(quantity)
        if quantity < 0:
            raise ValueError
    except ValueError:
        flash("Quantity must be 0 or greater", "Error")
        return redirect(url_for("seller.add_inventory"))

    image_file = request.files.get("image")
    image_filename = None
    safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    if image_file and image_file.filename != "":
        ext = os.path.splitext(image_file.filename)[1]
        image_filename = f"{safe_name}_{get_utc_now().strftime('%Y_%m_%d_%H_%M_%S')}{ext}"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        image_file.save(image_path)

    seller_id = session.get("user_id")

    new_item = Inventory(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        image=image_filename,
        seller_id=seller_id,
    )

    try:
        with Session(engine) as db_session:

            db_session.add(new_item)
            db_session.commit()
            db_session.refresh(new_item)

            flash(f"Inventory item '{new_item.name}' added successfully", "Success")
            logger.info(f"Inventory added by seller {seller_id}: {new_item.name}")
            return redirect(url_for("seller.dashboard"))

    except Exception as e:
        logger.exception(str(e))
        flash(str(e), "Error")
        return redirect(url_for("inventory.add_inventory"))


@seller.route("/delete-inventory/<int:item_id>", methods=["POST"])
@login_required
@role_required("seller", "admin")
def delete_inventory(item_id: int):
    seller_id = session.get("user_id")
    try:
        with Session(engine) as db:
            item = db.exec(
                select(Inventory).where(
                    Inventory.id == item_id,
                    Inventory.seller_id == seller_id,
                    Inventory.is_active == True,
                )
            ).one_or_none()

            if not item:
                message = "Inventory item not found or access denied"
                flash(message, "Error")
                logger.warning(message)
                return redirect(url_for("seller.dashboard"))

            item.is_active = False
            item.updated_at = get_utc_now()

            db.add(item)
            db.commit()
            db.refresh(item)

            message = f"Inventory '{item.name}' removed successfully"
            flash(message, "Success")
            logger.info(message)

    except Exception as e:
        logger.exception(str(e))
        flash("Failed to delete inventory item", "Error")

    return redirect(url_for("seller.dashboard"))


@seller.route("/update-inventory/<int:item_id>", methods=["GET", "POST"])
@role_required("seller")
def update_inventory(item_id: int):
    seller_id = session.get("user_id")

    with Session(engine) as db:
        inventory = db.exec(
            select(Inventory).where(
                Inventory.id == item_id,
                Inventory.seller_id == seller_id,
                Inventory.is_active == True,  # noqa
            )
        ).one_or_none()

        if not inventory:
            message = "Inventory item not found"
            flash(message, "Error")
            logger.warning(message)
            return redirect(url_for("seller.dashboard"))

        if request.method == "GET":
            return render_template("seller/update_inventory.html", inventory=inventory, )

        try:
            inventory.name = request.form.get("name").strip()
            inventory.description = request.form.get("description").strip()
            inventory.price = float(request.form.get("price"))
            inventory.quantity = int(request.form.get("quantity"))
            inventory.updated_at = get_utc_now()

            image_file = request.files.get("image")
            safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', inventory.name)
            if image_file and image_file.filename != "":
                ext = os.path.splitext(image_file.filename)[1]
                image_filename = f"{safe_name}_{get_utc_now().strftime('%Y_%m_%d_%H_%M_%S')}{ext}"
                image_path = os.path.join(UPLOAD_FOLDER, image_filename)
                old_image_path = os.path.join(UPLOAD_FOLDER, inventory.image)
                image_file.save(image_path)
                inventory.image = image_filename
                os.remove(old_image_path)

            db.add(inventory)
            db.commit()
            db.refresh(inventory)

            flash("Inventory updated successfully", "Success")
            logger.info(f"Inventory updated: {inventory.id}")

        except Exception as e:
            db.rollback()
            logger.exception(str(e))
            flash("Failed to update inventory", "Error")

    return redirect(url_for("seller.dashboard"))
