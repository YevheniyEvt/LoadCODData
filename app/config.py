"""
Configuration and const
"""
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from decouple import config as con


DEBUG = False
TEST = con('TEST', cast=bool, default=False)

BASE_DIR = Path(__file__).parent

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
USERNAME = con('DATABASE_USERNAME')
PASSWORD = con('DATABASE_PASSWORD')
HOST = con('DATABASE_HOSTNAME')
PORT = con('DATABASE_PORT')
DATABASE = con('DATABASE_NAME')

DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    database=DATABASE,
)
ECHO = False

if TEST or DEBUG:
    DATABASE_URL = "sqlite+pysqlite:///:memory:"
    ECHO = True

ENGINE = create_engine(DATABASE_URL, echo=ECHO)

# all for testing
PLAYER_DATA_IMAGE = BASE_DIR / 'test' / 'images' / 'player_data.png'
PLAYER_INFO_IMAGE = BASE_DIR / 'test' / 'images' / 'player_info.png'
ALLIANCE_INFO_IMAGE = BASE_DIR / 'test' / 'images' / 'alliance_info.png'
CUSTOM_CONFIG = r'--oem 3 --psm 6'