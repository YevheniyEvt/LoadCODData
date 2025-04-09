
import pytest
import pytesseract
import sys
import platform
from unittest.mock import MagicMock
from sqlalchemy.orm import Session, sessionmaker

from app import config
from app.models import Base, Season, Alliance, Player

if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'



sys.modules['pyautogui'] = MagicMock()

@pytest.fixture(name='engine')
def create_test_engine():
    test_engine = config.ENGINE
    Base.metadata.create_all(test_engine)
    yield test_engine
    Base.metadata.drop_all(test_engine)

@pytest.fixture(name='session')
def create_session(engine):
    session = Session(engine)
    yield session
    session.close()


@pytest.fixture(name='player_data')
def create_player_data()->str:
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(config.PLAYER_DATA_IMAGE, config=custom_config)
    return text

@pytest.fixture(name='player_info')
def create_player_info()->str:
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(config.PLAYER_INFO_IMAGE, config=custom_config)
    return text

@pytest.fixture(name='alliance_info')
def create_alliance_info()->str:
    custom_config = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(config.ALLIANCE_INFO_IMAGE, config=custom_config)
    return text

@pytest.fixture(name='create_season')
def create_season(session):
    season = Season(name='SoS4-6014')
    session.add(season)
    session.commit()

@pytest.fixture(name='create_alliance')
def create_alliance(session):
    alliance = Alliance(name='Tested alliance', short_name='D~C', server=100)
    session.add(alliance)
    session.commit()

@pytest.fixture(name='create_player')
def create_player(session):
    player = Player(game_id=100000, name='Test Player')
    session.add(player)
    session.commit()
    session.close()

