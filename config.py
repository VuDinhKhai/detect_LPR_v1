import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')

db_engine = create_engine(f'mysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}', pool_size=20)

current_directory = os.getcwd()

weights_detect=current_directory + os.environ.get('detect_LP')
weights_reco = current_directory + os.environ.get('reco_LP')
weights_tracking = current_directory + os.environ.get('tracking')
config_strongsort = current_directory + os.environ.get('config_strongsort')

image_directory = 'image_mysql'

file_log = current_directory + os.environ.get('file_log')

MAX_BUFFER_SIZE = 50