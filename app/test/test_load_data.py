
import pytesseract

from app.load_data import load_player_data, load_player_info, load_alliance_info

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'


IMAGE_DIR = '/app/test/images\\'
PLAYER_DATA_IMAGE = 'C:\\MyProects\\LoadCODData\\app\\test\\images\\player_data.png'
PLAYER_INFO_IMAGE ='C:\\MyProects\\LoadCODData\\app\\test\\images\\player_info.png'
ALLIANCE_INFO_IMAGE = f'C:\\MyProects\\LoadCODData\\app\\test\\images\\alliance_info.png'

def scan_screen(screen)->str:
    custom_config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(screen, config=custom_config)
    return text


def test_load_player_info():
    text = scan_screen(PLAYER_INFO_IMAGE)
    player_info = load_player_info(text)
    assert 'alliance' in player_info
    assert 'power' in player_info
    assert 'merits' in player_info


def test_load_player_data():
    text = scan_screen(PLAYER_DATA_IMAGE)
    player_data = load_player_data(text)
    assert "highest_power" in player_data
    assert "victories" in player_data
    assert "defeats" in player_data
    assert "city_sieges" in player_data
    assert "killed" in player_data
    assert "healed" in player_data
    assert "power" in player_data

def test_load_alliance_info():
    text = scan_screen(ALLIANCE_INFO_IMAGE)
    alliance_data = load_alliance_info(text)
    assert 'server' in alliance_data
    assert 'short_name' in alliance_data
    assert 'name' in alliance_data