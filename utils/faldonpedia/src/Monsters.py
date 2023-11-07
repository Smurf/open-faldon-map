from sqlalchemy import Boolean, Integer, String

from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from AbstractBase import Base
from dataclasses import dataclass


from Items import Item

@dataclass
class Monster(Base):
    __tablename__ = "monsters"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    exp: Mapped[int] = mapped_column(Integer())
    hit_points: Mapped[int] = mapped_column(Integer())
    mana_points: Mapped[int] = mapped_column(Integer())
    armor_class: Mapped[int] = mapped_column(Integer())
    armor_class: Mapped[int] = mapped_column(Integer())
    lore_min: Mapped[int] = mapped_column(Integer())
    lore_max: Mapped[int] = mapped_column(Integer())
    taming_min: Mapped[int] = mapped_column(Integer())
    taming_max: Mapped[int] = mapped_column(Integer())
    damage_min: Mapped[int] = mapped_column(Integer())
    damage_max: Mapped[int] = mapped_column(Integer())
    critical_min: Mapped[int] = mapped_column(Integer())
    critical_max: Mapped[int] = mapped_column(Integer())
    resistances: Mapped[JSON] = mapped_column(JSON)
    religion: Mapped[int] = mapped_column(Integer())
    religion_exp: Mapped[int] = mapped_column(Integer())

class MonsterDrops(Base):
    __tablename__ = "monster_drops"
    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    monster_id: Mapped[int] = mapped_column(Integer(), ForeignKey('monsters.id'))
    item_id: Mapped[int] = mapped_column(Integer(), ForeignKey('items.id'))
    amount: Mapped[int] = mapped_column(Integer())
    chance: Mapped[str] = mapped_column(String())
