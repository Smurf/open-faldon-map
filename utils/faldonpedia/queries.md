weapons.html
```
SELECT i.id,
		i.name,
        w.minimum_damage,
        w.maximum_damage,
        json_extract(e.requirements, '$.str') AS str_req,
        json_extract(e.requirements, '$.def') AS def_req,
        json_extract(e.requirements, '$.con') AS con_req,
        json_extract(e.requirements, '$.int') AS int_req,
        json_extract(e.requirements, '$.stam') AS stam_req,
        json_extract(e.requirements, '$.mag') AS mag_req,
        json_extract(e.requirements, '$.level') AS level_req,
        json_extract(e.stat_mods, '$.str') AS str_mod,
        json_extract(e.stat_mods, '$.def') AS def_mod,
        json_extract(e.stat_mods, '$.con') AS con_mod,
        json_extract(e.stat_mods, '$.int') AS int_mod,
        json_extract(e.stat_mods, '$.stam') AS stam_mod,
        json_extract(e.stat_mods, '$.mag') AS mag_mod,
        json_extract(e.resistances, '$.lightning') AS lightning_res,
        json_extract(e.resistances, '$.fire') AS fire_res,
        json_extract(e.resistances, '$.poison') AS poison_res,
        json_extract(e.resistances, '$.holy') AS holy_res,
        json_extract(e.resistances, '$.magic') AS magic_res,
        json_extract(e.resistances, '$.paralysis') AS paralysis_res,
        i.weight
        FROM items i JOIN equipable e USING (id) JOIN weapons w using (id) WHERE i.type = 1;

```

items.html
```
SELECT i.id,
		i.name,
        json_extract(e.requirements, '$.str') AS str_req,
        json_extract(e.requirements, '$.def') AS def_req,
        json_extract(e.requirements, '$.con') AS con_req,
        json_extract(e.requirements, '$.int') AS int_req,
        json_extract(e.requirements, '$.stam') AS stam_req,
        json_extract(e.requirements, '$.mag') AS mag_req,
        json_extract(e.requirements, '$.level') AS level_req,
        json_extract(e.stat_mods, '$.str') AS str_mod,
        json_extract(e.stat_mods, '$.def') AS def_mod,
        json_extract(e.stat_mods, '$.con') AS con_mod,
        json_extract(e.stat_mods, '$.int') AS int_mod,
        json_extract(e.stat_mods, '$.stam') AS stam_mod,
        json_extract(e.stat_mods, '$.mag') AS mag_mod,
        e.block,
        json_extract(e.resistances, '$.lightning') AS lightning_res,
        json_extract(e.resistances, '$.fire') AS fire_res,
        json_extract(e.resistances, '$.poison') AS poison_res,
        json_extract(e.resistances, '$.holy') AS holy_res,
        json_extract(e.resistances, '$.magic') AS magic_res,
        json_extract(e.resistances, '$.paralysis') AS paralysis_res,
        i.weight
        FROM items i JOIN equipable e USING (id) WHERE i.type != 1;

```

drops.html

```
SELECT 	m.id,
		m.name,
        m.hit_points,
        m.mana_points,
        m.exp,
        i.name,
		m_d.amount,
        m_d.chance  
    FROM monster_drops m_d inner join monsters m on m_d.monster_id = m.id Inner Join items i on m_d.item_id = i.id;
```

monsters.html
```
SELECT 	*
	FROM monsters;
```
