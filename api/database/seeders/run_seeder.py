from api.db import SessionLocal
from .seeders import SeederRunner

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
