#! env python3

# builtin imports
import sys
sys.path.insert(0, "./src")

from typing import Tuple
import json

# sqlalchemy imports
from sqlalchemy import create_engine
from sqlalchemy import select, join, text
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship

# class imports
from Monsters import Monster, MonsterDrops
from Items import Item, ItemTypeTable, ItemType, Equipable, Weapon
from AbstractBase import Base
import re

def read_file(filename:str)->str:
    lines = []
    with open(filename, "r") as f:
        line = f.readline()
        while line:
            lines.append(line)
            line = f.readline()

    return lines

def pull_colon_field(line:str)->int:

    return int(line.split(":")[-1].strip())

def pull_range_field(line:str):
    
    int_range = line.split(":")[-1].split("to")

    return int(int_range[0]), int(int_range[1])

def add_spaces(text):
    pattern = r"([A-Z][a-z]+)"
    return re.sub(pattern, r"\1 ", text)

def get_item_id_by_name(item_name:str, engine):
    session = Session(engine)

    if(re.match("^Ring \d", item_name)):
        item_name = "Ring"

    if(re.match("^Arrow Plus \d", item_name)):
        item_name = item_name.replace("Plus ", "+")
    
    if(item_name == "Padded Plate"):
        item_name = "Platinum Plate"

    if(item_name == "Royal Mage Robe"):
        item_name = "Royal Mages Robe"

    if(item_name == "Daemon Soccer Ball"):
        item_name = "Daemon"

    if(item_name == "Titan Claymore"):
        item_name = "Claymore Of Burning"

    if(item_name == "Master Sword"):
        item_name = "Claymore Of Burning"
    
    if(item_name == "Potion Of Light"):
        item_name = "Potion Of Experience"

    if(item_name == "Elixir Of Light"):
        item_name = "Elixir Of Experience"

    if(item_name == "Fragile Blade Of Chaos"):
        item_name = "Swordbreaker"
    
    if(item_name == "Ice Dagger"):
        item_name = "Ice Katar"

    if(item_name == "Master Sword"):
        item_name = "Gamemaster Sword"

    query = text(f"""SELECT i.id
    FROM items i INNER JOIN item_type i_t ON i.type = i_t.id JOIN equipable e USING (id) 
    WHERE name = "{item_name}";
    """)

    with engine.connect() as con:
        try:
            return con.execute(query).first()[0]
        except:
            return None


def main():

    engine = create_engine("sqlite:///./db/objects.sqlite", echo=True)
    Base.metadata.create_all(engine)
    # We have to do this because of sqlalchemy magic
    # If this isn't done the tables aren't automatically created
    from Monsters import Monster, MonsterDrops
    from Items import Item, ItemTypeTable, ItemType, Equipable, Weapon
    
    monsters = []
    drops = []
    lines = read_file("data/drops.txt")
    current_monster = Monster()
    current_mob_id = 1
    current_drop_id = 0
    on_drops = False
    for line in lines:
        #line = line.lower()
        if(on_drops):
            #Check for newline separator, if so we're off drops, skip
            if(line == "\n"):
                on_drops = False
            else:
                drop = line.split()
                item_name = add_spaces(drop[0]).rstrip()
                item_id = get_item_id_by_name(item_name, engine)
                if(item_id == None):
                    print(f"Couldn't find item {item_name}")
                    pass
                drop_chance = drop[2]

                t_drop = MonsterDrops()
                t_drop.id = current_drop_id
                t_drop.item_id = item_id
                t_drop.monster_id = current_mob_id
                t_drop.chance = drop_chance

                drops.append(t_drop)
                current_drop_id += 1
        if bool(re.search("Stats", line)):
            #if(on_drops): #If we were on drops last we hit a now mob
            #    on_drops = False
            #    monsters.append(current_monster)
            current_monster = Monster()
            current_monster.name = " ".join(line.split()[:-1])
            current_monster.id = current_mob_id
            current_mob_id += 1
            current_monster_res = {}
        if bool(re.search("Experience:", line)):    
            current_monster.exp = pull_colon_field(line) 
        if bool(re.search("HP:", line)):           
            current_monster.hit_points = pull_colon_field(line)
        if bool(re.search("Mana:", line)):          
            current_monster.mana_points = pull_colon_field(line)
        if bool(re.search("Lore ", line)):          
            current_monster.lore_min, current_monster.lore_max = pull_range_field(line)
        if bool(re.search("Taming Range", line)):
            current_monster.taming_min, current_monster.taming_max = pull_range_field(line)
        if bool(re.search("Damage Min", line)):    
            current_monster.damage_min = pull_colon_field(line)
        if bool(re.search("Damage Max", line)):    
            current_monster.damage_min = pull_colon_field(line)
        if bool(re.search("Critical Hit Min", line)):
            current_monster.critical_min = pull_colon_field(line)
        if bool(re.search("Critical Hit Max", line)):
            current_monster.critical_max = pull_colon_field(line)
        if bool(re.search("Cold Resist", line)):          
            current_monster_res['cold'] = pull_colon_field(line)
        if bool(re.search("Fire Resist", line)):          
            current_monster_res['fire'] = pull_colon_field(line)
        if bool(re.search("Lightning Resist", line)):
            current_monster_res['lightning'] = pull_colon_field(line)
        if bool(re.search("Physical Resist", line)):      
            current_monster_res['physical'] = pull_colon_field(line)
        if bool(re.search("Holy Resist", line)):          
            current_monster_res['holy'] = pull_colon_field(line)
        if bool(re.search("Magic Resist", line)):         
            current_monster_res['magic'] = pull_colon_field(line)
        if bool(re.search("Religion:", line)):     
            current_monster.religion = pull_colon_field(line)
        if bool(re.search("Item Drops", line)):
            current_monster.resistances = current_monster_res.copy()
            monsters.append(current_monster)
            on_drops = True
    with Session(engine) as session:
        session.add_all(monsters)
        session.add_all(drops)
        session.commit()
    
if __name__ == "__main__":
    main()
