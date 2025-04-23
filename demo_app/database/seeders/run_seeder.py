from demo_app.db import SessionLocal
from demo_app.database.seeders.seeders import SeederRunner

def main():
    db = SessionLocal()
    try:
        with db.begin():
            SeederRunner().run(db)
            db.commit()
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main() 
