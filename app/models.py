"""
Models to create table in database
"""
from reprlib import repr
from datetime import datetime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, BigInteger, DateTime

from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "player_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(unique=True, index=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)

    alliance_id: Mapped[Optional[int]] = mapped_column(ForeignKey("alliance.id"))
    alliance: Mapped["Alliance"] = relationship(back_populates="players")

    data: Mapped[List["PlayerData"]] = relationship(back_populates="player", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Player(id: {self.game_id}, name: {self.name}, alliance: {self.alliance_id})"


class Alliance(Base):
    __tablename__ = 'alliance'

    id: Mapped[int] = mapped_column(primary_key=True)
    server: Mapped[int]
    name: Mapped[str] = mapped_column(String(30), unique=True)
    short_name: Mapped[str] = mapped_column(String(5), unique=True)

    players: Mapped[List["Player"]] = relationship(back_populates="alliance", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Alliance(name: {self.short_name}, server: {self.server})"


class PlayerData(Base):
    __tablename__ = "player_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    add_date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    highest_power: Mapped[int] = mapped_column(BigInteger)
    power: Mapped[int] = mapped_column(BigInteger)
    merits: Mapped[int] = mapped_column(BigInteger)
    city_sieges: Mapped[int]
    killed: Mapped[int] = mapped_column(BigInteger)
    healed: Mapped[int] = mapped_column(BigInteger)
    victories: Mapped[int] = mapped_column(BigInteger)
    defeats: Mapped[int] = mapped_column(BigInteger)
    dead: Mapped[int] = mapped_column(BigInteger)

    player_id = mapped_column(ForeignKey("player_info.id"))
    player: Mapped["Player"] = relationship(back_populates="data")

    season_id = mapped_column(ForeignKey("season.id"))
    season: Mapped["Season"] = relationship(back_populates="player_data")

    def __repr__(self):
        represent = (f"PlayerData(player: {self.player},"
                     f" add_date: {self.add_date},"
                     f" power: {self.power},"
                     f" merits: {self.merits})"
                     )
        return represent



class Season(Base):
    __tablename__ = "season"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    start: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    end: Mapped[Optional[datetime]] = mapped_column(DateTime)

    player_data: Mapped[List["PlayerData"]] = relationship(back_populates="season", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Season(name: {self.name}, start: {self.start})"

