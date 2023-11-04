# objects.dat reverse engineering

# Items

* Items are 0x1f3 (499) bytes long
* **All values below are offsets from 0x0 of the 499 byte chunk of an item.**

# Item Name


|    Value    | Address Range | Encoding |  Type  |
|:-----------:|:-------------:|:--------:|:------:|
|  Item Name  |   0x00-0x18   |   utf-8  | uint8 |
| Plural Name |   0x19-0x31   |   utf-8  | uint8 |


# Item Type


|     Type    | Address | Value |  Type  | Note                                      |
|:-----------:|:-------:|:-----:|:------:|-------------------------------------------|
|    Normal   |   0x36  |   01  | uint8 | [Weapon Type](#weapon-type) must be zero. |
|    Sword    |   0x36  |   01  | uint8 |                                           |
|     Ring    |   0x36  |   02  | uint8 | [Weapon Type](#weapon-type) must be zero. |
|    Shield   |   0x36  |   03  | uint8 |                                           |
|  Head Armor |   0x36  |   04  | uint8 |                                           |
|  Body Armor |   0x36  |   05  | uint8 |                                           |
|    Torch    |   0x36  |   06  | uint8 |                                           |
|    Unused   |   0x36  |   07  | uint8 |                                           |
|    Potion   |   0x36  |   08  | uint8 |                                           |
|  Spellbook  |   0x36  |   09  | uint8 |                                           |
|     Rune    |   0x36  |   0A  | uint8 |                                           |
|   Sailboat  |   0x36  |   0B  | uint8 |                                           |
|    Unused   |   0x36  |   0C  | uint8 |                                           |
|     Ammo    |   0x36  |   0D  | uint8 |                                           |
|  Gauntlets  |   0x36  |   0E  | uint8 |                                           |
|  Hairstyle  |   0x36  |   0F  | uint8 |                                           |
	

## Equippable Item Data

All equipables have these values.

### Uniqueness

#### Unique Item
If an item is unique two uint8 values are set.

| Address | Value |  Type  |
|:-------:|:-----:|:------:|
|   0x64  |   FF  | uint8 |
|   0x65  |   FF  | uint8 |

#### Lost Artifact
The following value is set if the item is a lost artifact.

| Address | Value |  Type  |
|:-------:|:-----:|:------:|
|   0xAD  |   01  | uint8 |


### Requirements
Stat and level requirments for an equippable item. 
Behaves as expected, value is value.

|  Stat | Address |  Type  |
|:-----:|:-------:|:------:|
|  Str  |   0x37  | uint16 |
|  Def  |   0x8b  | uint16 |
|  Con  |   0x89  | uint16 |
|  Int  |   0x39  | uint16 |
|  Stam |   0x3b  | uint16 |
|  Mag  |   0x8d  | uint16 |
| Level |   0x97  | uint16 |

### Stat Boosts
Values start at 0x7F, increments for each + stat.

|  Stat | Address |  Type  |
|:-----:|:-------:|:------:|
|  Str  |   0x53  | int8 |
|  Def  |   0x54  | int8 |
|  Con  |   0x55  | int8 |
|  Int  |   0x52  | int8 |
|  Stam |   0x51  | int8 |
|  Mag  |   0x56  | int8 |

### Resistances
These use an odd type that's like an opposite of an int8. It represents -127-128 BUT it's backwards?
If these values are > 0x7F (127) 0x100 (256) must be subtracted to get the correct value.

|  Resistance | Address |  Type  |
|:-----------:|:-------:|:------:|
|  Lightning  |   0xA1  | sint8 |
|     Fire    |   0xA3  | sint8 |
|    Poison   |   0xA7  | sint8 |
|     Holy    |   0xA9  | sint8 |
|    Magic    |   0xA5  | sint8 |
|  Paralysis  |   0xAB  | sint8 |

## Weapon Item Data
Weapons have unique information about their type and handedness.

### Weapon Type

|     Type     | Address | Value |  Type  |
|:------------:|:-------:|:-----:|:------:|
| unclassified |   0x47  |   00  | uint8 |
|     Sword    |   0x47  |   01  | uint8 |
|     Mace     |   0x47  |   02  | uint8 |
|      Axe     |   0x47  |   03  | uint8 |
|     Staff    |   0x47  |   04  | uint8 |
|      Bow     |   0x47  |   05  | uint8 |

### Weapon Type Attributes
Additional weapon attributes are 00/01 values.

|     Type    | Address |  Type  |
|:-----------:|:-------:|:------:|
|  Projectile |   0x48  | uint8 |
|    Silver   |   0x49  | uint8 |
|  Two handed |   0x88  | uint8 |
|    Cursed   |   0x4A  | uint8 |

### Weapon Stats 
|      Stat      | Address |  Type  |
|:--------------:|:-------:|:------:|
| Minimum Damage |   0x4B  | uint8 |
| Maximum Damage |   0x4C  | uint8 |
|  Attack Rating |   0x45  | uint8 |

# Misc Values

- 0x32 - weight
    - Used by telekinesis. 
