from sqlalchemy import create_engine

# DB config
DB_USER = "vehicle-identification"
DB_PASS = "aipt2023"
DB_HOST = "localhost"
DB_NAME = "vehicle-identification"

db_engine = create_engine(f'mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}')