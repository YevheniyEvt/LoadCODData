"""
All what need to scan screen
"""
import pytesseract
import pyautogui
import config

pytesseract.pytesseract.tesseract_cmd = config.PYTESSERACT_PATH

def scan_screen(region=None)->str:
    """
        Make screenshot. For func load_player_info and
        load_alliance_info have specific region to have more clean data
        :param region:
        :return: str
    """
    screen = pyautogui.screenshot(region=region)
    text = pytesseract.image_to_string(screen, config=config.TO_STRING_CONFIG)
    return text

def get_alliance_info_coord():
    """
        Check coord for screenshot. It will be
        region for func scan_screen. Need prepare
        image that coord will be checked
     """
    screen = pyautogui.locateOnScreen(config.IMAGE_TO_REGION_ALLIANCE)
    print(screen)

def get_player_info_coord():
    """
        Check coord for screenshot. It will be
        region for func scan_screen. Need prepare
        image that coord will be checked
    """
    screen = pyautogui.locateOnScreen(config.IMAGE_TO_REGION_PLAYER)
    print(screen)
