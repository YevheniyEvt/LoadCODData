"""
Configuration and const
"""
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from decouple import config


DEBUG = False

# Image and coord to load player info data
IMAGE_TO_REGION_PLAYER = '../images/check_stat.png'
PLAYER_INFO_COORD = (700, 200, 890, 320)

# Image and coord to load alliance info data
IMAGE_TO_REGION_ALLIANCE = '../images/alliance.png'
ALLIANCE_INFO_COORD = (720, 215, 411, 182)

# Tesseract configurations
PYTESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract'
TO_STRING_CONFIG = r'--oem 3 --psm 6'

# Database configurations
USERNAME = config('DATABASE_USERNAME')
PASSWORD = config('DATABASE_PASSWORD')
HOST = config('DATABASE_HOSTNAME')
PORT = config('DATABASE_PORT')
DATABASE = config('DATABASE_NAME')
DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    database=DATABASE,
)
TEST_URL = "sqlite+pysqlite:///:memory:"

if DEBUG:
    DATABASE_URL = TEST_URL

ENGINE = create_engine(DATABASE_URL, echo=False)