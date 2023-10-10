# .content-main
import time
import requests
import os
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup

def load_monster_dict(monster_list_path):
  dict = {}
  with open(monster_list_path, "r") as f:
    for line in f:
      line = line.strip()
      if line:
        monster_id, monster_name = line.split(",")
        monster_name = monster_name.lower()
        dict[monster_name] = monster_id
  return dict

page = requests.get('https://www.faldonrpg.com/encyclopedia/list_monsters.php')

soup = BeautifulSoup(page.content, "html.parser")

main_content = soup.find(class_="content-main")
monster_links = main_content.find_all("a")

monster_ids = load_monster_dict("../../monsters.txt")

for link in monster_links:
    monster_id = parse_qs(urlparse(f"https://www.faldonrpg.com/encyclopedia/{link['href']}").query)['id'][0]
    if not os.path.exists(f"../../images/mob-art/{monster_id}.png"):
        monster_page = requests.get(f"https://www.faldonrpg.com/encyclopedia/{link['href']}")
        soup = BeautifulSoup(monster_page.content, "html.parser")

        monster_name = soup.find(class_="content-main").find_all("table")[1].find_all("b")[0].text.strip().lower()

        #Typo on page
        if(monster_name == "mirthril slime"): monster_name = "mithril slime"

        print(f"Found {monster_name}, scraping...")
        print(f"Found ID {monster_ids[monster_name]} for {monster_name}")
        try:
            monster_img_elem = soup.find(class_="content-main").find_all("table")[0].find_all("img")[0]
            monster_img = requests.get(f"https://www.faldonrpg.com/{monster_img_elem['src']}")
        
            open(f"../../images/mob-art/{monster_id}.png", "wb").write(monster_img.content)
        except:
            continue
    else:
        print("Mob already found, skipping")
    time.sleep(1)
