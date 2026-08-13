from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


DATABASE_URL = "postgresql://postgres:postgres@127.0.0.1:5433/personal_inbox"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)