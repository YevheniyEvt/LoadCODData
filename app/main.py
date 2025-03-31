"""
Run program
"""

import config
from models import Base
from database import create_player_data as run


def create_table():
    Base.metadata.create_all(config.ENGINE)

if __name__ == '__main__':
    print('Start')
    if config.DEBUG:
        create_table()
    run()
