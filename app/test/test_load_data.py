
import datetime
from unittest.mock import patch

from sqlalchemy import select

from app.models import Alliance, Player, PlayerData
from app.load_data import load_player_data, load_player_info, load_alliance_info
from app.database import create_alliance_data, create_player_data, create_player_info


def test_load_alliance_info():
    alliance_data = load_alliance_info()
    assert 'server' in alliance_data
    assert 'short_name' in alliance_data
    assert 'name' in alliance_data

def test_load_player_info():
    player_info = load_player_info()
    assert 'alliance' in player_info
    assert 'power' in player_info
    assert 'merits' in player_info

def test_load_player_data():
    player_data = load_player_data()
    assert "highest_power" in player_data
    assert "victories" in player_data
    assert "defeats" in player_data
    assert "city_sieges" in player_data
    assert "killed" in player_data
    assert "healed" in player_data
    assert "power" in player_data

def test_create_alliance_data(session):
    create_alliance_data(session=session)
    alliance = session.scalar(select(Alliance)
                              .where(Alliance.name == 'Demons of Chaos')
                              )
    assert alliance.name == 'Demons of Chaos'
    assert alliance.short_name == 'D~C'



def test_create_player_info(create_alliance, session):
    paste_sequence = iter([
        "",
        "10000",
        "Testname",
        "Testname",
    ])

    def fake_paste():
        return next(paste_sequence)
    with patch('pyperclip.paste', side_effect=fake_paste):
        create_player_info(session=session)

        player_info = session.scalar(select(Player)
                                     .where(Player.game_id == 10000)
                                     )
        assert player_info.name == 'Testname'
        assert player_info.alliance.short_name == 'D~C'
        assert player_info.alliance.name == 'Tested alliance'

def test_create_player_data(create_player, session):
    with patch('pyperclip.paste', return_value=100000):
        create_player_data(session=session)
        stmt = (
            select(PlayerData)
            .join(PlayerData.player)
            .where(Player.game_id == 100000)
        )
        player_data_db = session.scalars(stmt).first()
        assert player_data_db.merits == 350632
        assert player_data_db.power == 117905975
        assert player_data_db.highest_power == 129971875
        assert player_data_db.city_sieges == 220
        assert player_data_db.killed == 610313412
        assert player_data_db.healed == 274898704
        assert player_data_db.victories == 104145
        assert player_data_db.defeats == 46502
        assert player_data_db.dead == 780254
        assert player_data_db.season_id == 1
        assert player_data_db.add_date.date() == datetime.datetime.now().date()