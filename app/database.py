"""
Prepare and load data to database
"""
from datetime import datetime
import time
import pyperclip
from dataclasses import dataclass, field, asdict

import sqlalchemy.exc
from sqlalchemy.orm import Session
from sqlalchemy import select, func

import load_data
import config
from models import Player, PlayerData, Alliance, Season


SessionConnected = Session(config.ENGINE)

@dataclass
class PlayerInfo:
    """Prepare data for ORM model Player"""

    game_id: int = field(default=None)
    name: str = field(default=None)
    alliance: Alliance = field(default=None)

    def player_id(self):
        """
            When scanned screen we copy player id
            in game. Here pasted it.
        """
        try:
            self.game_id = int(pyperclip.paste())
            print(f'id: {self.game_id} was saved')
        except ValueError:
            ...

    def player_name(self):
        """
            When scanned screen we copy
            player nickname. Here pasted it.
        """
        past_name = pyperclip.paste()
        try:
            int(past_name)
        except ValueError:
            if past_name:
                self.name = pyperclip.paste()
                print(f'name: {self.name} was saved')


@dataclass
class PreparePlayerData:
    """Prepare data for ORM model PlayerData"""

    highest_power: int = field(default=None)
    power: int = field(default=None)
    city_sieges: int = field(default=None)
    killed: int = field(default=None)
    healed: int = field(default=None)
    victories: int = field(default=None)
    defeats: int = field(default=None)
    dead: int = field(default=None)
    merits: int | None = field(default=None)
    player: Player = field(default=None)
    season_id: int = field(default=1)

    def from_dict(self, data: dict):
        for key, value in data.items():
            self.__dict__[key] = value

def create_season():

    season = Season(name='SoS4-6014')
    with SessionConnected as session:
        session.add(season)
        session.commit()

def check_player_data_database(player_game_id: int) -> bool:
    """
        Check! was player data saved to database today?
        :param player_game_id: int
        :return: bool
    """
    with (SessionConnected as session):
        player = session.scalar(select(Player).where(Player.game_id == player_game_id))
        player_db = session.execute(select(PlayerData)
                                    .where(PlayerData.player == player)
                                    .where(func.date(PlayerData.add_date) == datetime.now().date())
                                    ).first()
        if player_db is not None:
            print(f'Data{player_db} is already saved!')
            time.sleep(2)
        return player_db is not None


def create_alliance_data()-> Alliance:
    """
        Get data from scanned screen,
        then save data in database alliance table.
        :return: Alliance
    """
    run = True
    while run:
        alliance_data = load_data.load_alliance_info()
        alliance = Alliance(**alliance_data)
        if alliance_data.get('short_name', None) is not None:
            smt = select(Alliance).where(
                Alliance.short_name == alliance_data.get('short_name', None)
            )
            with SessionConnected as session:
                try:
                    session.scalars(smt).one()
                except sqlalchemy.exc.NoResultFound:
                    session.add(alliance)
                    session.commit()
                    print(alliance)
        return alliance

def create_player_info() -> Player:
    """
        Get data from scanned screen,
        prepare it in PlayerInfo dataclass,
        then save data in database player_info table
        and return Player instance
        :return: Player
    """
    print('Start create new player')
    player_info = PlayerInfo()
    while player_info.game_id is None:
        player_info.player_id()

    print('Wait for copy player name...')
    while player_info.name is None:
        player_info.player_name()

    smt = select(Player).where(
        Player.game_id == player_info.game_id)
    try:
        with SessionConnected as session:
            session.scalars(smt).one()
    except sqlalchemy.exc.NoResultFound:

        print(f'Load {player_info.name} alliance...')
        while player_info.alliance is None:
            with SessionConnected as session:
                load_info = load_data.load_player_info()
                alliance = session.scalar(select(Alliance).where(
                        Alliance.short_name == load_info.get('alliance')))
                if alliance is None:
                    alliance = create_alliance_data()
                player_info.alliance = alliance

        with SessionConnected as session:
            player = Player(**asdict(player_info))
            session.add(player)
            session.commit()
            print(f'Player: {player} saved!')
    return player

def create_player_data()-> None:
    """
        Get data from scanned screen,
        prepare it in PlayerInfo dataclass,
        then save data in database player_data table.
        If player info do not saved to database yet
        run create_player_info func.
        Player id we copy in game then paste here.
        To stop running program just copy 'stop'
        :return: None
    """
    print('Load player data')
    run = True
    previous_player_id = 0
    while run:

        player_data = PreparePlayerData()
        print('Wait for copy player id or copy "stop" to STOP program...')
        while player_data.player is None:
            if str(pyperclip.paste()).lower() == 'stop':
                run = False
                print('Stop scanning')
                break

            try:
                int(pyperclip.paste())
            except ValueError:
                continue

            player_id = int(pyperclip.paste())
            data_in_database = check_player_data_database(player_id)
            if  data_in_database:
                continue

            if player_id != previous_player_id:
                smt = select(Player).where(
                    Player.game_id == player_id)
                try:
                    with SessionConnected as session:
                        player = session.scalars(smt).one()
                        player_data.player = player

                except sqlalchemy.exc.NoResultFound:
                    player_data.player = create_player_info()
        if not run:
            break
        while player_data.merits is None:
            player_data.merits = load_data.load_player_info().get('merits', None)
        print('Wait for load player data...')
        while None in asdict(player_data).values():
            data = load_data.load_player_data()
            player_data.from_dict(data)

        with SessionConnected as session:
            player_data_db = PlayerData(**asdict(player_data))
            session.add(player_data_db)
            session.commit()
            previous_player_id = player_data_db.player.game_id
            print(f'{player_data_db} saved!')

















