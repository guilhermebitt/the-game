# COMO USAR ESTE CÓDIGO

# CHAME ELE USANDO EQUIPAMENT(ARG1,ARG2)

# ARG1 = TIPO DE EQUIPAMENTO ('armor','weapon','artifact','soul','potion')

# ARG2 = NIVEL DO EQUIPAMENTO (DE 1 A 10) ou ate mais :) ...

# RETORNA UM DICIONARIO COM O NOME DO ITEM, O STAT QUE ELE AUMENTA E A QUANTIDADE AUMENTADA

from secrets import randbelow

class Equipament():
    def __init__(self,category,level) -> None:
        if category == 'random':
            categories = ['artifact', 'weapon', 'armor', 'soul', 'potion']
            self.category = categories[randbelow(5)]
        else:
            self.category = category
        self.level = level
        match self.category:
            case 'artifact':
                self.get = Artifact.get_item(self)
            case 'weapon':
                self.get = Weapon.get_item(self)
            case 'armor':
                self.get = Armor.get_item(self)
            case 'soul':
                self.get = Soul.get_item(self)
            case 'potion':
                self.get = Potion.get_item(self)
    
    def excess(self):
        if self.level > 10:
            excess = self.level - 10
            self.level = 10
            return excess
        return 0
        
    def returnal(self, name, stat, increase, category='random'):
        category = self.category
        return {'name': name, 'stat': stat, 'increase': increase, 'category': category}


class Armor(Equipament):
    def get_item(self):
        excess = self.excess()
        stat = 'defense'
        id = {
        1: 'Leather Armor',
        2: 'Chainmail Armor',
        3: 'Plate Armor',
        4: 'Iron Armor',
        5: 'Golden Armor',
        6: 'Tungsten Armor',
        7: 'Diamond Armor',
        8: 'Neon Armor',
        9: 'Dragon Armor',
        10: 'Celestial Armor',
            }
        id = id.get(self.level)
        return self.returnal(id + '+'*excess,stat,self.level*2 + excess*2)
    

class Weapon(Equipament):
    def get_item(self):
        excess = self.excess()
        stat = 'attack'
        id = {
        1: 'Training Sword',
        2: 'Iron Sword',
        3: 'Axe',
        4: 'Silver Sword',
        5: 'Silver Lance',
        6: 'WarAxe',
        7: 'Diamond Lance',
        8: 'Giant Hammer',
        9: 'Dragon Axe',
        10: 'Celestial Naginata'
            }
        id = id.get(self.level)
        return self.returnal(id + '+'*excess,stat,self.level*2 + excess*2)


class Artifact(Equipament):
    def get_item(self):
        excess = self.excess()
        stat = 'health'
        id = {
        1: 'Ancient stone',
        2: 'Silver amulet',
        3: 'Bloody Demon Tooth',
        4: 'Mysterious Eye',
        5: 'Golden Chalice',
        6: 'Dragon Heart',
        7: 'Celestial Crystal',
        8: 'Moon Orb',
        9: 'Tiny Planet',
        10: 'Pocket Star'
            }
        id = id.get(self.level)
        return self.returnal(id + '+'*excess,stat,self.level*10 + excess*10)
    

class Soul(Equipament):
    def get_item(self):
        excess = self.excess()
        stat = 'attack and defense'
        id = {
        1: 'Spirit Anchor',
        2: 'Phantom Gyroscope',
        3: 'Serpent Soul',
        4: 'Spectral Chain',
        5: 'Essence Core',
        6: 'Wraith Orb',
        7: 'Ethereal Pentagon',
        8: 'Crystal of Souls',
        9: 'Astral Star',
        10: 'Gatekeeper Soul'
            }
        id = id.get(self.level)
        return self.returnal(id + '+'*excess,stat,self.level*2 + excess*2)
    

class Potion(Equipament):
    def get_item(self):
        excess = self.excess()
        id = {
        1: ('FireHeart potion','-defense +attack',2),
        2: ('FrozenSoul potion','+defense -attack',2),
        3: ('Storm Potion','+defense +attack',2),
        4: ('Midas potion','+money',15),
        5: ('Grand Healing Potion','+heal',30),
        6: ('Massive Healing Potion','+heal',45),
        7: ('Extreme Healing Potion','+heal',60),
        8: ('Dragon Blood Potion','+heal',75),
        9: ('Regeneration Cells','+heal',100),
        10: ('Mysteryous Liquid','+ap recover',10)
            }
        id = id.get(self.level)
        return self.returnal(id[0] + '+'*excess,id[1],id[2] + excess*5)


#print(Equipament("soul",1).get)
