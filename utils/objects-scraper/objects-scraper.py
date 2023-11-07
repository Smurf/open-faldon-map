#! env python3

# builtin imports
import sys
sys.path.insert(0, "./src")

from typing import Tuple
import json

# sqlalchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# class imports
from Items import Item, ItemTypeTable, ItemType, Equipable, Weapon
from AbstractBase import Base


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

def main():
    objects = read_file('./data/objects.dat')
    with open('./json/object-schema.json', 'r') as f:
        schema_dict = json.loads(f.read())
    
    engine = create_engine("sqlite:///./db/objects.sqlite", echo=True)
    Base.metadata.create_all(engine)
    # We have to do this because of sqlalchemy magic
    # If this isn't done the tables aren't automatically created
    from Items import Item, ItemTypeTable, ItemType, Equipable, Weapon

    chunks = chunkify(objects)
    weapons = []
    equipable = []
    for obj_id, obj in enumerate(chunks):
        parsed_object = Item(obj_id+1, obj, schema_dict)
        match ItemType(parsed_object.item_data['item_type']):
            case ItemType.WEAPON:
                weapons.append(Weapon(obj_id+1, obj, schema_dict))
            case _:
                equipable.append(Equipable(obj_id+1, obj, schema_dict))
    with Session(engine) as session:
        init_item_type_table(session)
        session.add_all(equipable)
        session.add_all(weapons)
        session.commit()

if __name__ == "__main__":
    main()
