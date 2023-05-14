import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(find_dotenv())

vk_token = os.getenv('VK_TOKEN')
user_token = os.getenv('USER_TOKEN')

user = os.getenv('User', 'postgres')
password = os.getenv('Password', '1331')
db_name = os.getenv('db_name', 'inderbot')
localhost = os.getenv('localhost')
port = os.getenv('port', 5432)

DSN = f'postgresql://{user}:{password}@{localhost}:{port}/{db_name}'

engine = create_engine(DSN)


Session = sessionmaker(bind=engine)
db = Session()

db.close()
