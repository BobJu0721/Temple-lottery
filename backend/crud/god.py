from sqlalchemy.orm import Session
from backend.models.god import God

def get_gods(db: Session):
    return db.query(God).all()

def get_god_by_id(db: Session, god_id: int):
    return db.query(God).filter(God.id == god_id).first()
