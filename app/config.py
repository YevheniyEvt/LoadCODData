"""
Configuration and const
"""

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from decouple import config as con


DEBUG = True
TEST = True

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
USERNAME = con('DATABASE_USERNAME', default ='')
PASSWORD = con('DATABASE_PASSWORD', default ='')
HOST = con('DATABASE_HOSTNAME', default ='')
PORT = con('DATABASE_PORT', default ='')
DATABASE = con('DATABASE_NAME', default ='')
if USERNAME:
    POSTGRES_DATABASE = URL.create(
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
    ECHO = True
else:
    DATABASE_URL = POSTGRES_DATABASE
    ECHO = False

ENGINE = create_engine(DATABASE_URL, echo=ECHO)


# all for testing
PLAYER_DATA_IMAGE = '..\\app\\test\\images\\player_data.png'
PLAYER_INFO_IMAGE ='..\\app\\test\\images\\player_info.png'
ALLIANCE_INFO_IMAGE = '..\\app\\test\\images\\alliance_info.png'
CUSTOM_CONFIG = r'--oem 3 --psm 6'