from sqlalchemy import create_engine
from app.models import Base

DATABASE_URL = "postgresql://user:pass@db:5432/mydb"
engine = create_engine(DATABASE_URL)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
