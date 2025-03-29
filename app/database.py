"""
Prepare and load data to database
Param in function with default None -
it`s parameter for test.
If test is running func take them else it`s None
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

def generate_session():
    while True:
        with Session(config.ENGINE) as session:
            yield session

SessionConnected = generate_session()


@dataclass
class PlayerInfo:
    """Prepare data for ORM model Player"""

    game_id: int = field(default=None)
    name: str = field(default=None)
    alliance_id: int = field(default=None)

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
    player_id: int = field(default=None)
    season_id: int = field(default=1)


    def __call__(self, **kwargs):
        self.__dict__.update(kwargs)

def create_season()->None:
    season = Season(name='SoS4-6014')
    session = next(SessionConnected)
    session.add(season)
    session.commit()

def check_player_data_database(player_game_id: int, session=None) -> bool:
    """
        Check! was player data saved to database today?
        :param player_game_id: int
        :param session: Session
        :return: bool

    """
    if session is None:
        session = next(SessionConnected)
    stmt = (
        select(PlayerData)
        .join(PlayerData.player)
        .where(Player.game_id == player_game_id)
        .where(func.date(PlayerData.add_date) == datetime.now().date())
    )
    player_data_db = session.scalars(stmt).first()
    if player_data_db is not None:
        time.sleep(0.3)
    return player_data_db is not None

def create_alliance_data(session:Session = None)-> Alliance:
    """
        Get data from scanned screen,
        then save data in database alliance table.
        :param session: Session
        :return: Alliance
    """
    if session is None:
        session = next(SessionConnected)
    while True:
        alliance_data = load_data.load_alliance_info()
        smt = (select(Alliance).
               where(Alliance.short_name == alliance_data.get('short_name', None))
               )
        try:
            alliance= session.scalars(smt).one()
            return alliance
        except sqlalchemy.exc.NoResultFound:

            alliance = Alliance(**alliance_data)
            session.add(alliance)
            session.commit()
        return alliance

def create_player_info(session:Session = None) -> Player:
    """
        Get data from scanned screen,
        prepare it in PlayerInfo dataclass,
        then save data in database player_info table
        and return Player instance
        :param session: Session
        :return: Player
    """
    print('Start create player')
    player_info = PlayerInfo()
    if session is None:
        session = next(SessionConnected)
    while player_info.game_id is None:
        player_info.player_id()

    smt = (select(Player)
           .where(Player.game_id == player_info.game_id)
           )

    try:
        player = session.scalars(smt).one()

        return player
    except sqlalchemy.exc.NoResultFound:
        print('Wait for copy player name...')
        while player_info.name is None:
            player_info.player_name()

        print(f'Load {player_info.name} alliance...')
        while player_info.alliance_id is None:
            alliance = create_alliance_data(session=session)
            player_info.alliance_id = alliance.id

        player = Player(**asdict(player_info))
        session.add(player)
        session.commit()
        print(f'Player: {player} saved!')
        return player

def create_player_data(session:Session = None)-> None:
    """
        Get data from scanned screen,
        prepare it in PlayerInfo dataclass,
        then save data in database player_data table.
        If player info do not saved to database yet
        run create_player_info func.
        Player id we copy in game then paste here.
        To stop running program just copy 'stop'
        :return: None
        :param session: Session

    """
    print('Load player data')
    run = True
    previous_player_id = 0
    while run:
        player_data = PreparePlayerData()
        print('Wait for copy player id or copy "stop" to STOP program...')
        while player_data.player_id is None:
            if str(pyperclip.paste()).lower() == 'stop':
                run = False
                print('Stop scanning')
                break

            try:
                int(pyperclip.paste())
            except ValueError:
                continue

            player_id = int(pyperclip.paste())
            data_in_database = check_player_data_database(player_game_id=player_id, session=session)
            if  data_in_database:
                continue

            if player_id != previous_player_id:
                player_data.player_id = create_player_info(session=session).id

        if not run:
            break

        while player_data.merits is None:
            player_data.merits = load_data.load_player_info().get('merits', 0)

        print('Wait for load player data...')
        while None in asdict(player_data).values():
            data = load_data.load_player_data()
            player_data(**data)

        if session is None:
            session = next(SessionConnected)

        player_data_db = PlayerData(**asdict(player_data))
        session.add(player_data_db)
        session.commit()
        previous_player_id = player_data_db.player.game_id
        print(f'{player_data_db} saved!')

        if config.TEST:
            session.close()
            run = False


















