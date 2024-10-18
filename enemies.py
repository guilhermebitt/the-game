from secrets import randbelow

class Enemy():
    def __init__(self, id, player_defense):
        self.id = id
        self.actions_color = 'ffffff'
        self.p_deff = player_defense
        self.entry_phrase = 'None'

    def choose(self):
        enemy_classes = {
            1: Vase,
            2: MagicVase,
        }
        if self.id in enemy_classes:
            return enemy_classes[self.id](self.p_deff)
        else:
            return None
        
    def reduce_e_life(self, damage):
        self.life = str(int(self.life) - damage)
        text = 'None'
        return text


class Vase(Enemy):
    def __init__(self, player_defense):
        super().__init__(2, player_defense)
        self.life = '15'
        self.atk = '10'
        self.deff = '5'
        self.name = '"The Chosen One"'
        self.turns = 2
        self.img = 'assets/images/enemies/vase.png'
        self.color = '8a6442'
        # IMPORTANT: loot order -> MONEY, SPELL, ITEM
        self.loot = {"money": randbelow(21), "item": 1}

    def do_action(self):
        choice = randbelow(100) + 1  # 1 to 100
        if choice > 5:
            action = self.simple_attack()
            type = 'attack'
        elif choice > 2:
            action = self.phrase1()
            action = f'[color={self.color}]{action}[/color]'
            type = 'dialogue'
        elif choice >= 0:
            action = self.miss()
            type = 'dialogue'
        return action, type

    def simple_attack(self):
        damage = int(self.atk) - self.p_deff
        if damage < 0:
            damage = 0
        text = f'The enemy attacked! You take [color={self.actions_color}]{damage}[/color] points of damage.'
        return damage, text

    def phrase1(self):
        text = "THE CHOSEN ONE: My purpose is not to contain water... it is to contain destiny. And yours, it's about to overflow."
        return text
    
    def miss(self):
        text = "The enemy's attack miss you."
        return text


class MagicVase(Enemy):
    def __init__(self, player_defense):
        super().__init__(2, player_defense)
        self.life = '10'
        self.atk = '15'
        self.deff = '5'
        self.name = '"Magic Vase"'
        self.turns = 3
        self.img = 'assets/images/enemies/magic_vase.png'
        self.color = '7c40b8'
        # IMPORTANT: loot order -> MONEY, SPELL, ITEM
        self.loot = {"money": randbelow(41)+10, "spell": randbelow(10)+1}

    def do_action(self):
        choice = randbelow(100) + 1  # 1 to 100
        if choice > 7:
            action = self.fireball()
            type = 'attack'
        elif choice >= 3:
            action = self.simple_attack()
            type = 'attack'
        elif choice == 2:
            action = self.miss()
            type = 'dialogue'
        elif choice == 1:
            action = self.phrase1()
            action = f'[color={self.color}]{action}[/color]'
            type = 'dialogue'
        elif choice == 0:
            action = self.phrase2()
            action = f'[color={self.color}]{action}[/color]'
            type = 'dialogue'
        return action, type

    def simple_attack(self):
        damage = int(self.atk) - self.p_deff
        if damage < 0:
            damage = 0
        text = f'The enemy attacked! You take [color={self.actions_color}]{damage}[/color] points of damage.'
        return damage, text

    def fireball(self):
        damage = (int(self.atk)* 1.5) - self.p_deff
        text = f'The enemy casted [FIREBALL]. You take [color={self.actions_color}]{int(damage)}[/color] points of damage.'
        if damage < 0:
            damage = 0
        return damage, text
    
    def miss(self):
        text = "MAGIC VASE: The enemy's attack miss you."
        return text

    def phrase1(self):
        text = "MAGIC VASE: I am the receptacle of the impossible, the chalice of the unknown. The oldest magic rests within me."
        return text

    def phrase2(self):
        text = "MAGIC VASE: My runes glow with ancient secrets. Only those worthy can understand the power I hold."
        return text
