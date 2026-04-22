from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine, Base
from backend.models.god import God
from backend.models.fortune_content import FortuneContent
from backend.models.admin_user import AdminUser
from backend.crud.admin import get_password_hash

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # Create Admin
        if not db.query(AdminUser).filter_by(username="admin").first():
            admin = AdminUser(username="admin", hashed_password=get_password_hash("admin123"))
            db.add(admin)
            print("Admin user created (admin / admin123)")

        # Create Gods
        gods_data = [
            {"name": "天上聖母 (媽祖)", "description": "保佑海上平安、消災解厄"},
            {"name": "關聖帝君", "description": "保佑事業順利、財源廣進"},
            {"name": "城隍爺", "description": "明辨是非、保佑地方安寧"}
        ]
        
        for g_data in gods_data:
            god = db.query(God).filter_by(name=g_data["name"]).first()
            if not god:
                god = God(name=g_data["name"], description=g_data["description"])
                db.add(god)
                db.commit()
                db.refresh(god)
                print(f"God '{god.name}' created.")

                # Seed 60 fortunes for this god
                for i in range(1, 61):
                    fc = FortuneContent(
                        god_id=god.id,
                        fortune_no=i,
                        level="大吉" if i % 5 == 0 else "中吉", # Just dummy data
                        poem=f"第{i}籤詩文內容：海闊天空任遨遊，順風順水好行舟",
                        career_interp="事業發展順利",
                        love_interp="感情和睦",
                        health_interp="身體健康",
                        study_interp="學業進步"
                    )
                    db.add(fc)
                db.commit()
                print(f"60 fortunes created for '{god.name}'.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
    print("Database seeding completed.")
