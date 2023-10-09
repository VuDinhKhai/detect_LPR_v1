import os
from dotenv import load_dotenv
load_dotenv()
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')



current_directory = os.getcwd()

weights_detect=current_directory + os.environ.get('detect_LP')
weights_reco = current_directory + os.environ.get('reco_LP')

image_directory = 'image_mysql'