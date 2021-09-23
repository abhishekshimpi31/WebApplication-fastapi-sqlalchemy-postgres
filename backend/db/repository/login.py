from sqlalchemy.orm import Session
from db.models.user import Users


def get_user(username: str, db: Session):
    user = db.query(Users).filter(username == Users.email).first()
    return user
