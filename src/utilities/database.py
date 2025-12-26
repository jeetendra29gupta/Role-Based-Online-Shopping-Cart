import os

from sqlmodel import SQLModel
from sqlmodel import Session
from sqlmodel import create_engine
from sqlmodel import select

from src.models.user import UserRole
from src.utilities.config import Config
from src.utilities.logger import get_logger
from src.utilities.security import hash_password

logger = get_logger(__name__)
os.makedirs(Config.DATABASE_DIR, exist_ok=True)
database_path = f"{Config.DATABASE_DIR}/{Config.DATABASE_NAME}"
database_url = f"sqlite:///{database_path}"

engine = create_engine(database_url, echo=False)


def init_table():
    from src.models.user import User  # noqa

    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as db_session:
        existing_user = db_session.exec(select(User).where(User.id == 1)).first()
        if existing_user:
            logger.info("Admin already exists")
            return

        admin_user = User(
            full_name="Jeetendra Gupta",
            email_id="jeetendra29gupta@gmail.com",
            hashed_password=hash_password("jeetendra29gupta"),
            phone_no="9555613730",
            role=UserRole.ADMIN,
        )

        db_session.add(admin_user)
        db_session.commit()
        db_session.refresh(admin_user)

        logger.info("Admin created successfully")
