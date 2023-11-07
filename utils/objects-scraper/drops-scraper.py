#! env python3

# builtin imports
import sys
sys.path.insert(0, "./src")
import re

# sqlalchemy imports
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import Session

# class imports
from Monsters import Monster, MonsterDrops
from Items import Item, ItemTypeTable, ItemType, Equipable, Weapon
from AbstractBase import Base

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
    
    renames = [
            ("Padded Plate", "Platinum Plate"),
            ("Royal Mage Robe", "Royal Mages Robe"),
            ("Pink Mage Robe", "Pink Mages Robe"),
            ("Greater Mage Robe", "Greater Mages Robe"),
            ("Daemon Soccer Ball", "Daemon"),
            ("Titan Claymore", "Claymore Of Burning"),
            ("Master Sword", "Gamemaster Sword"),
            ("Potion Of Light", "Potion Of Experience"),
            ("Elixir Of Light", "Elixir Of Experience"),
            ("Ice Dagger", "Ice Katar"),
            ("Druid Helm", "Druid Hat"),
            ("Druid Vestment", "Druid Vestments"),
            ("Blood Star", "Bloodstar"),
            ("Pink Hand Axe", "Pink Handaxe"),
            ("Storm Breaker", "Stormbreaker"),
            ("Spartan Gloves", "Spartan Gauntlets"),
            ("Armor of Helios", "Armor Of Helios"),
            ("Soulshield", "Souls Shield"),
            ("Souls Helm", "Souls Helmet"),
            ("Large Rejuinvation Potion", "Elixir Of Rejuinvation"),
            ("GMRUNE", "Gmrune"),
            ("Fragile Blade Of Chaos", "Swordbreaker")
            ]
    for rename in renames:
        if(item_name == rename[0]):
            #print(f"Replaced {item_name} with {rename[1]}")
            item_name = rename[1]

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

    engine = create_engine("sqlite:///./db/faldon-data.sqlite", echo=False)
    Base.metadata.create_all(engine)
    # We have to do this because of sqlalchemy magic
    # If this isn't done the tables aren't automatically created
    from Monsters import Monster, MonsterDrops
    from Items import Item, ItemTypeTable, ItemType, Equipable, Weapon
    
    monsters = []
    drops = []
    lines = read_file("data/drops.txt")
    current_monster = Monster()
    current_mob_id = 0
    current_drop_id = 0
    on_drops = False
    for line in lines:
        #line = line.lower()
        if(on_drops):
            #Check for newline separator, if so we're off drops, skip
            if(line == "\n"):
                on_drops = False

                current_mob_id += 1
            else:
                drop = line.split()
                item_name = add_spaces(drop[0]).rstrip()
                item_id = get_item_id_by_name(item_name, engine)
                if(item_id == None):
                    print(f"Couldn't find item {item_name}")
                else:
                    drop_chance = drop[2]
                
                    t_drop = MonsterDrops()
                    t_drop.id = current_drop_id
                    t_drop.item_id = item_id
                    t_drop.monster_id = current_mob_id
                    t_drop.amount = int(drop[1])+1
                    t_drop.chance = drop_chance

                    drops.append(t_drop)
                    current_drop_id += 1

        line = line.lower()
        if bool(re.search("stats", line)):
            current_monster = Monster()
            current_monster.name = " ".join(line.split()[:-1]).title()
            current_monster.id = current_mob_id
            current_monster_res = {}
        if bool(re.search("experience:", line)):    
            current_monster.exp = pull_colon_field(line) 
        if bool(re.search("hp:", line)):           
            current_monster.hit_points = pull_colon_field(line)
        if bool(re.search("armor class:", line)):
            current_monster.armor_class = pull_colon_field(line)
        if bool(re.search("mana:", line)):          
            current_monster.mana_points = pull_colon_field(line)
        if bool(re.search("lore range", line)):          
            current_monster.lore_min, current_monster.lore_max = pull_range_field(line)
        if bool(re.search("taming range", line)):
            current_monster.taming_min, current_monster.taming_max = pull_range_field(line)
        if bool(re.search("damage min", line)):    
            current_monster.damage_min = pull_colon_field(line)
        if bool(re.search("damage max", line)):    
            current_monster.damage_max = pull_colon_field(line)
        if bool(re.search("critical hit min", line)):
            current_monster.critical_min = pull_colon_field(line)
        if bool(re.search("critical hit max", line)):
            current_monster.critical_max = pull_colon_field(line)
        if bool(re.search("cold resist", line)):          
            current_monster_res['cold'] = pull_colon_field(line)
        if bool(re.search("fire resist", line)):          
            current_monster_res['fire'] = pull_colon_field(line)
        if bool(re.search("lightning resist", line)):
            current_monster_res['lightning'] = pull_colon_field(line)
        if bool(re.search("physical resist", line)):      
            current_monster_res['physical'] = pull_colon_field(line)
        if bool(re.search("holy resist", line)):          
            current_monster_res['holy'] = pull_colon_field(line)
        if bool(re.search("magic resist", line)):         
            current_monster_res['magic'] = pull_colon_field(line)
        if bool(re.search("religion kills", line)):
            current_monster.religion_exp = pull_colon_field(line)
        if bool(re.search("religion:", line)):     
            current_monster.religion = pull_colon_field(line)
        if bool(re.search("item drops", line)):
            current_monster.resistances = current_monster_res.copy()
            monsters.append(current_monster)
            on_drops = True

    with Session(engine) as session:
        session.add_all(monsters)
        session.add_all(drops)
        session.commit()
    
if __name__ == "__main__":
    main()
