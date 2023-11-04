#! env python3

from ItemParserMixin import ItemParserMixin
from enum import Enum
from typing import ByteString, Tuple, ForwardRef
import json
from sqlalchemy import Boolean, MetaData, Integer, String, Table

from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, JSON
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
#from sqlalchemy.schema import MetaData

Base = declarative_base()

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
        print(self.type)
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


def read_file(filename:str)->bytes:
    with open(filename, "rb") as f:
        data = f.read()

    return data

# read bin data until a specific byte
def read_until(bin_data:bytes, search_byte:bytes)-> Tuple[bytearray, bytes] | None:
    data = bytearray()
    for i in range(len(bin_data)):
        byte = bin_data[i].to_bytes()
        rest_bytes = bin_data[i:]
        if byte.hex() == search_byte.hex():
            print('found end byte')
            break
        byte = int.from_bytes(byte, byteorder='big', signed=False)
        data.append(byte)
    return (data, rest_bytes)

def chunkify(object_data:bytearray):
    """Splits a bytearray into 499 byte chunks.

    Args:
        object_data : A bytearray object.

    Returns:
        A list of bytearray objects, each containing 499 bytes.
    """

    num_chunks = len(object_data) // 499
    chunks = []

    for i in range(num_chunks):
        start = i * 499
        end = start + 499
        chunk = object_data[start:end]
        chunks.append(chunk)

    return chunks

def init_item_type_table(session):

    for idx,current_type in enumerate(ItemType):
        session.add(ItemTypeTable(type=current_type.name, id=idx))

    session.commit()

def init_relationships():
    Item.equipable = relationship(
        Equipable,
        back_populates="item",
        uselist=False,
    )

    Equipable.item = relationship(
        Item,
        back_populates="equipable",
        uselist=False,
    )

    Weapon.equipable = relationship(
        Equipable,
        back_populates="equipable",
        uselist=False,
    )
def main():
    objects = read_file('./data/objects.dat')
    with open('./json/object-schema.json', 'r') as f:
        schema_dict = json.loads(f.read())

    init_relationships()
    chunks = chunkify(objects)
    weapons = []
    equipable = []
    armor = []
    accessories = []
    for obj_id, obj in enumerate(chunks):
        parsed_object = Item(obj_id+1, obj, schema_dict)
        match ItemType(parsed_object.item_data['item_type']):
            case ItemType.WEAPON:
                weapons.append(Weapon(obj_id+1, obj, schema_dict))
            case _:
                equipable.append(Equipable(obj_id+1, obj, schema_dict))
    engine = create_engine("sqlite:///./db/objects.sqlite", echo=True)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        init_item_type_table(session)
        session.add_all(equipable)
        session.add_all(weapons)
        session.commit()

    with engine.connect() as conn:
        stmt = select(Item)
        #for row in conn.execute(stmt):
            #print(row)
if __name__ == "__main__":
    main()
