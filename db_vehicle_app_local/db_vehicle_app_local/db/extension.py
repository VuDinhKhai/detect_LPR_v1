from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import db_engine

db_base_model = declarative_base()
db_session = sessionmaker(bind = db_engine)
