from ItemParserMixin import ItemParserMixin

from enum import Enum
from sqlalchemy import Boolean, Integer, String

from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, JSON
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from AbstractBase import Base

class ItemType(Enum):
    NORMAL = 0
    WEAPON = 1
    RING = 2
    SHIELD = 3
    HEAD = 4
    BODY = 5
    TORCH = 6
    UNUSED = 7
    POTION = 8
    SPELLBOOK = 9
    RUNE = 10
    SAILBOAT = 11
    UNUSED2 = 12
    AMMO = 13
    GAUNTLETS = 14
    HAIRSTYLE = 15
    BOOTS = 16
    LOCKED_DOWN = 17
    DEATH_SKULL = 18
    SOCCER_BALL = 19
    SCROLL = 20
    SHURIKEN = 21
    CAPE = 22
    GREAVES = 23

class ItemTypeTable(Base):
    __tablename__ = "item_type"

    id = mapped_column(Integer(), primary_key=True, unique=True)
    type: Mapped[str] = mapped_column((String()))

class Item(ItemParserMixin,Base):

    __tablename__ = "items"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    #type: Mapped[int] = mapped_column(Integer())
    type: Mapped[int] = mapped_column(Integer(), ForeignKey("item_type.id"))
    name: Mapped[str] = mapped_column(String(24))
    plural_name: Mapped[str] = mapped_column(String(24))
    weight: Mapped[int] = mapped_column(Integer())

    def __init__(self, obj_id:int, bin_data:bytearray, schema:dict):
        self.item_data = {}
        self.bin_data = bin_data
        self.schema = schema
        self.schema_part = "item"
        self.parse_per_schema(self.item_data, self.schema, self.schema_part)

        # Assigning mapped values
        self.id = obj_id
        self.name = self.item_data['name']
        self.type = self.item_data['item_type']
        self.plural_name = self.item_data['plural_name']
        self.weight = self.item_data['weight']


class Equipable(Item):
    __tablename__ = "equipable"
    id : Mapped[int] = mapped_column(Integer(), ForeignKey("items.id"), primary_key=True)
    unique: Mapped[bool] = mapped_column(Boolean())
    lost_artifact: Mapped[bool] = mapped_column(Boolean())
    requirements: Mapped[JSON] = mapped_column(JSON)
    stat_mods: Mapped[JSON] = mapped_column(JSON)
    resistances: Mapped[JSON] = mapped_column(JSON)

    def __init__(self, obj_id, bin_data:bytearray, schema:dict):
        super().__init__(obj_id, bin_data, schema)
        self.schema_part = "equipable"
        self.schema = schema
        self.parse_per_schema(self.item_data, self.schema, self.schema_part)
        
        self.unique = self.item_data['unique'] == 255
        self.lost_artifact = self.item_data['lost_artifact'] == 1
        self.requirements = self.item_data['requirements']
        self.stat_mods = self.item_data['stat_mods']
        self.resistances = self.item_data['resistances']

class Weapon(Equipable):
    __tablename__ = "weapons"
    id = mapped_column(Integer(), ForeignKey("equipable.id"), primary_key=True)
    weapon_type: Mapped[int] = mapped_column(Integer())
    minimum_damage: Mapped[int] = mapped_column(Integer())
    maximum_damage: Mapped[int] = mapped_column(Integer())
    attack_rating: Mapped[int] = mapped_column(Integer())
    type_attributes: Mapped[JSON] = mapped_column(JSON)
    def __init__(self, obj_id, bin_data:bytearray, schema:dict):
        super().__init__(obj_id, bin_data, schema)
        self.schema_part = "weapon"
        self.schema = schema
        self.parse_per_schema(self.item_data, self.schema, self.schema_part)
        #print(f"weapons stat_mods: {self.stat_mods}")
        self.weapon_type = self.item_data['weapon_type']
        self.minimum_damage = self.item_data['minimum_damage']
        self.maximum_damage = self.item_data['maximum_damage']
        self.attack_rating = self.item_data['attack_rating']
        self.type_attributes = self.item_data['type_attributes']


