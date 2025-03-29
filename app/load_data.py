"""
Scan screen and load data from screenshot
"""

import config
from scan_and_read import scan_screen



def load_player_data(text=None)->dict:
    """
        Load data from screenshot
        :param text:
        :return: dict
    """
    if text is None:
        text = scan_screen(func='player_data')
    clear_text = text[text.find('Historical'):text.find('Gathered')].split('\n')
    data_dict = {}

    for data in clear_text:
        match data.split():
            case data if 'Historical' in data:
                try:
                    data_dict["highest_power"] = int(data[-1].replace(',',''))
                except ValueError:
                    data_dict["highest_power"] = int(data[-2].replace(',',''))
            case data if 'Victories' in data:
                try:
                    data_dict["victories"] = int(data[-1].replace(',',''))
                except ValueError:
                    data_dict["victories"] = int(data[-2].replace(',',''))
            case data if 'Defeats' in data:
                try:
                    data_dict["defeats"] = int(data[-1].replace(',',''))
                except ValueError:
                    data_dict["defeats"] = int(data[-2].replace(',',''))
            case data if 'Sieges' in data:
                try:
                    data_dict["city_sieges"] = int(data[-1].replace(',',''))
                except ValueError:
                    data_dict["city_sieges"] = int(data[-2].replace(',',''))
            case data if "Killed" in data:
                try:
                    data_dict["killed"] = int(data[-1].replace(',',''))
                except ValueError:
                    data_dict["killed"] = int(data[-2].replace(',',''))
            case data if "Dead" in data:
                try:
                    data_dict["dead"] = int(data[-1].replace(',',''))
                except ValueError:
                    data_dict["dead"] = int(data[-2].replace(',',''))
            case data if "Healed" in data:
                try:
                    data_dict["healed"] = int(data[-1].replace(',',''))
                except ValueError:
                    data_dict["healed"] = int(data[-2].replace(',',''))
                try:
                    data_dict["power"] = int(data[0].replace(',',''))
                except ValueError:
                    data_dict["power"] = int(data[1].replace(',',''))
    return data_dict

def load_player_info(text=None) -> dict:
    """
        Load data from screenshot
        :param text: str
        :return: dict
    """
    if text is None:
        text = scan_screen(region=config.PLAYER_INFO_COORD, func='player_info')
    data_dict = {}
    clear_text = text[text.find('#'): text.find('Achievements')].split('\n')
    for data in clear_text:
        match data.split():
            case [power, merits]:
                try:
                    data_dict['power'] = int(power.replace(',', ''))
                    data_dict['merits'] = int(merits.replace(',', ''))
                except ValueError:
                    ...
            case [alliance, *_] if '[' in alliance:
                name = alliance.partition(']')
                index = name.index(']')
                try:
                    data_dict['alliance'] = name[index-1].strip('[')
                except ValueError:
                    ...
    return data_dict

def load_alliance_info(text=None)->dict:
    """
        Load data from screenshot
        :param text: str
        :return: dict
    """
    data_dict = {}
    if text is None:
        text = scan_screen(region=config.ALLIANCE_INFO_COORD, func='alliance')
    for data in text.split('\n'):
        match data:
            case data if '#' in data:
                try:
                    data_dict['server'] = data.strip('#')
                except ValueError:
                    ...
            case data if '[' in data and ']' in data:
                names = data.partition(']')
                index = names.index(']')
                try:
                    data_dict['short_name'] = names[index-1].strip('[')
                except ValueError:
                    ...
                try:
                    data_dict['name'] = names[index+1]
                except ValueError:
                    ...

    return data_dict


