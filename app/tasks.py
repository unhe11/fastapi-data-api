from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from . import crud, models, schemas

celery_app = Celery('tasks', broker='redis://redis:6379/0')

DATABASE_URL = "postgresql://user:pass@db:5432/mydb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@celery_app.task
def analyze_device_data_async(device_id: str, start_date: str = None, end_date: str = None) -> dict:
    db = SessionLocal()
    try:
        data_points = crud.get_device_data(db, device_id, start_date, end_date)
        result = crud.analyze_data(data_points)
        return result.dict()
    finally:
        db.close()
