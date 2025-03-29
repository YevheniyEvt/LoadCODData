"""
Run program
"""
from models import Base
import config

from database import create_player_data, create_alliance_data


def create_table():
    Base.metadata.create_all(config.ENGINE)

print(config.DATABASE_URL)
if __name__ == '__main__':
    print('Start')
    create_table()
    create_player_data()
