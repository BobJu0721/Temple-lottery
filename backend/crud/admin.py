from sqlalchemy.orm import Session
from passlib.context import CryptContext
from backend.models.admin_user import AdminUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_admin_by_username(db: Session, username: str):
    return db.query(AdminUser).filter(AdminUser.username == username).first()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
