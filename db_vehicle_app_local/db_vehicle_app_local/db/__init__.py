from .extension import db_base_model
from .config import db_engine
from .models import *

def create_db():
  try:
    db_base_model.metadata.create_all(db_engine)
  except Exception as e:
    pass