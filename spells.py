from random import randrange

class Category():
        def damage():
            return [1,2,4,5,6,7,8,9,10,11,12,15,16,17,18,19,20,21,22,23,24,26,27,28,29,30,31,33,34,35,36,37,38,39,40,42,44,45]
        def heal():
            return [3,13,14,17,34]
        def debuff_defense():
            return [5,15,29,32,38]
        def debuff_attack():
            return [7,18,30,32,38]
        def buff():
            return [25,41]
        def other():
            return [43,46,99]

rec_counter = 1
tb_counter = 8
ascended = False
opened = False

class Spells:
    def __init__(self, damage=['1','1'], defense=['1','1'], health=['1','1'], moves=['1','1'], id=0):
    #def __init__(self, damage, defense, health, moves, id):
        self.player_damage = int(damage[0])
        self.enemy_damage = int(damage[1])
        self.player_defense = int(defense[0])
        self.enemy_defense = int(defense[1])
        self.player_health = int(health[0])
        self.enemy_health = int(health[1])
        self.moves = moves
        self.id = id
        self.act = self.perform_action()

    def perform_action(self):
        action_method = list(self.get_action_method()[0])
        action_method.append(self.get_action_method()[1])
        action_method.append(self.get_action_method()[2])
        blocker = str(action_method[3]).find('-')
        try:
            if action_method[0] < 0:
                action_method[0] = 0
        except:
            pass
        if blocker != -1:
            action_method[3] = action_method[3][:blocker]  + '0 damage'''
        return action_method
            
    def get_action_method(self):
        return {
        1: (Common.fireball(self),'fire',f'Casts a fireball that does 1.5 times the damage | costs 1 action and 5 AP.'),
        2: (Common.lightning_bolt(self),'electricity',f'Casts a Lightning bolt that does 1.25 times the damage | costs 1 action and 3 AP.'),
        3: (Common.heal(self),'holy',f'Heals the player by 15 HP | costs 1 action and 7 AP.'),
        4: (Common.boulder(self),'earth',f'Create a boulder from the ground that does 2.0 times the damage | costs 2 action and 2 AP.'),
        5: (Common.acid(self),'acid',f'Create a small amount of acid that does damage and decreases the enemy defense by 2 | costs 1 action and 5 AP.'),
        6: (Common.burst(self),'electricity',f'Cast an small eletric explosion that does 2.25 times the damage | costs 1 action and 6 AP.'),
        7: (Common.iceball(self),'ice',f'Casts a iceball that does damage and decreases the enemy attack by 2 | costs 1 action and 5 AP.'),
        8: (Common.bomb(self),'N/A',f'Throws a bomb that does 2.75 times the damage | costs 2 action and 10 AP.'),
        9: (Common.rotating_disk(self),'air',f'Create a sharp disk that does 2.25 times the damage | costs 2 action and 7 AP.'),
        10: (Common.fire_charge(self),'fire',f'Charges toward the enemy covered in flames doing 2.5 times the damage | costs 2 action and 5 AP.'),
        11: (Rare.dark_fireball(self),'dark',f'Casts a fireball filled with evil that does 2.0 times the damage | costs 1 action and 5 AP.'),
        12: (Rare.thunderstorm(self),'electricity',f'Call down a thunderstorm that does 2.75 times the damage | costs 2 action and 4 AP.'),
        13: (Rare.prescise_heal(self),'holy',f'Concentrate to heal by 10 HP using less AP | costs 1 action and 4 AP.'),
        14: (Rare.greater_heal(self),'holy',f'Use a lot of AP to heal by 40 HP | costs 1 action and 5 AP.'),
        15: (Rare.corrosive_bubble(self),'acid',f'Casts a bubble of acid that does 1.3 times the damage and decreases the enemy defense by 4 | costs 2 action and 10 AP.'),
        16: (Rare.explosion(self),'fire',f"EXPLODE! doing 2.0 times the damage, don't worry, you will be fine | costs 1 action and 5 AP."),
        17: (Rare.life_steal(self),'dark',f'Steal the enemy health, dealing damage and recovering half of it | costs 1 action and 7 AP.'),
        18: (Rare.ice_blade(self),'ice',f'Wield an ice blade that does 1.75 times the damage and decreases the enemy attack by 4| costs 2 action and 10 AP.'),
        19: (Rare.bullet(self),'N/A',f"Shoot with a gun, that's it | costs 1 action and 1 AP."),
        20: (Rare.spirit_will(self),'holy',f'Casts a light from your will doing damage according to your health | costs 1 action and 4 AP.'),
        21: (Rare.laser(self),'electricity',f'Shoot an extremely fast laser from your finger doing 2.0 times the damage | costs 0 action and 10 AP.'),
        22: (Epic.invisible_cut(self),'dark',f'Cut the air ignoring half of the enemy defense and doing 2.7 times the damage | costs 1 action and 7 AP.'),
        23: (Epic.inferno(self),'fire',f'Cover the ground around you in flames doing 4.0 times the damage | costs 2 action and 12 AP.'),
        24: (Epic.recursion(self),'time',f'Create a sockwave that does 1.5 times the damage and increases the damage by each use | costs 2 action and 4 AP.'),
        25: (Epic.inner_power(self),'holy',f'Call a power from within increasing your stats by 1 | costs 2 action and 10 AP.'),
        26: (Epic.meteor(self),'earth',f'Call a meteor from space that does 3.0 times the damage | costs 1 action and 5 AP.'),
        27: (Epic.implosion(self),'fire',f'Cast an explosion from the enemy that does 3.5 times the damage and ignores half the defense | costs 2 action and 10 AP.'),
        28: (Epic.temporal_bolt(self),'time',f'Call a magic bolt from the future that does 1.5 times the damage and decreases the AP after each use | costs 1 action and 8 AP.'),
        29: (Epic.fracture(self),'earth',f'Shatter the air doing 3.0 times the damage and decreases the enemy defense | costs 2 action and 7 AP.'),
        30: (Epic.Typhoon(self),'air',f'Create a tornado that does 3.0 times the damage and decreases the enemy attack | costs 2 action and 7 AP.'),
        31: (Epic.temporal_reflexion(self),'time',f'Open a portal from the future, redirecting the enemy attack and doing damage to itself | costs 2 action and 8 AP.'),
        32: (Epic.weakening_curse(self),'dark',f'Cast a curse on the enemy, decreasing its defense and attack by 4 | costs 2 action and 10 AP.'),
        33: (Epic.chaos_magic(self),'time',f'Cast a chaotic bolt dealing random damage | costs 1 action and 4 AP.'),
        34: (Epic.syphon(self),'dark',f'Steal the enemy health, dealing damage and recovering all of it | costs 1 action and 10 AP.'),
        35: (Legendary.soul_pierce(self),'holy',f'Attack the enemy from inside dealing 2.5 times the damage | costs 1 action and 5 AP.'),
        36: (Legendary.spirit_cutter(self),'holy',f'Create a blade from your will doing damage according to your health | costs 1 action and 4 AP.'),
        37: (Legendary.stormbreak(self),'air',f'Split the sky destroing everything around you dealing 1.5 times the damage plus defense | costs 2 action and 8 AP.'),
        38: (Legendary.Hex(self),'dark',f'Casts a forbidden curse that does 2.5 times the damage and decreases the enemy attack and defense by 2 | costs 1 action and 10 AP.'),
        39: (Legendary.heaven_annihilation(self),'holy',f'Call heavenly retribution from above dealing 10 times the damage | costs 2 action and 25 AP.'),
        40: (Legendary.divide(self),'time',f'Divide the enemy in two, dealing half of the enemy health as damage | costs 2 action and 10 AP.'),
        41: (Legendary.evolve(self),'holy',f'Surpass your own nature, increasing your stats by 2 | costs 2 action and 15 AP.'),
        #0: (Legendary.wheel_of_fate,'N/A',f'Casts a completely random spell, good luck'),
        42: (Legendary.even_odd(self),'time',f'Cast a controled ball of chaos that deals big random damage | costs 1 action and 5 AP.'),
        43: (Legendary.reversal(self),'N/A',f"Change souls with the enemy, both gaining each other's health | costs 2 action and 20 AP."),
        44: (Legendary.blood_magic(self),'dark',f'Casts a ball of pure pain, increases the damage by health lost | costs 1 action and 5 AP.'),
        45: (Legendary.death(self),'N/A',f"Kill the enemy instantly, doesn't work on bosses however | costs 2 action and 60 AP."),
        46: (Legendary.ascencion(self),'holy',f'Ascend to new heights, only once | costs 2 action and 20 AP.'),
        99: (Legendary.gate_opener(self),'???',f'??? | costs 3 action.'),
    }.get(self.id)

class Common(Spells):
    def fireball(self):
        damage = int(self.player_damage * 1.5) - self.enemy_defense
        return damage, 1, 5, f'[FIREBALL] {damage} damage'
    
    def lightning_bolt(self):
        damage = int(self.player_damage * 1.25) - self.enemy_defense
        return damage, 1, 3, f'[LIGHTNINGBOLT] {damage} damage'
    
    def heal(self):
        return 15, 1, 7, f'[HEAL] recovered 15 HP'
    
    def boulder(self):
        damage = int(self.player_damage * 2.0) - self.enemy_defense
        return damage, 2, 2, f'[BOULDER] {damage} damage'
    
    def acid(self):
        damage = int(self.player_damage * 1.0) - self.enemy_defense
        defense = self.enemy_defense - 2
        if defense < 0:
            defense = 0
        return damage, 1, 5, f'[ACID] {damage} damage', defense
    
    def burst(self):
        damage = int(self.player_damage * 2.25) - self.enemy_defense
        return damage, 1, 6, f'[BURST] {damage} damage'

    def iceball(self):
        damage = int(self.player_damage * 1.0) - self.enemy_defense
        enemy_damage = self.enemy_damage - 2
        if enemy_damage < 1:
            enemy_damage = 1
        return damage, 1, 5, f'[ICEBALL] {damage} damage', 0,enemy_damage

    def bomb(self):
        damage = int(self.player_damage * 2.75) - self.enemy_defense
        return damage, 2, 10, f'[BOMB] {damage} damage'
    
    def rotating_disk(self):
        damage = int(self.player_damage * 2.5) - self.enemy_defense
        return damage, 2, 7, f'[ROTATINGDISK] {damage} damage'
    
    def fire_charge(self):
        damage = int(self.player_damage * 2.25) - self.enemy_defense
        return damage, 2, 5, f'[FIRECHARGE] {damage} damage'
    
class Rare(Spells):
    def dark_fireball(self):
        damage = int(self.player_damage * 2.0) - self.enemy_defense
        return damage, 1, 5, f'[DARKFIREBALL] {damage} damage'
    
    def thunderstorm(self):
        damage = int(self.player_damage * 2.75) - self.enemy_defense
        return damage, 2, 4, f'[THUNDERSTORM] {damage} damage'
    
    def prescise_heal(self):
        return 10, 1, 4, f'[PRESCISEHEAL] recovered 10 HP'
    
    def greater_heal(self):
        return 40, 1, 15, f'[GREATERHEAL] recovered 40 HP'
    
    def corrosive_bubble(self):
        damage = int(self.player_damage * 1.3) - self.enemy_defense
        defense = self.enemy_defense - 4
        if defense < 0:
            defense = 0
        return damage, 2, 10, f'[CORROSIVE BUBBLE] {damage} damage', defense
    
    def explosion(self):
        damage = int(self.player_damage * 2.0) - self.enemy_defense
        return damage, 1, 5, f'[EXPLOSION] {damage} damage'
    
    def life_steal(self):
        damage = int(self.player_damage * 1.0) - self.enemy_defense
        if damage < 1:
            return damage, 1, 7, f'[LIFE STEAL] {damage}', 0
        return damage, 1, 7, f'[LIFE STEAL] {damage} damage | recovered {int(damage/2)} HP',int(damage/2)

    def ice_blade(self):
        damage = int(self.player_damage * 1.75) - self.enemy_defense
        enemy_damage = self.enemy_damage - 2
        if enemy_damage < 1:
            enemy_damage = 1
        return damage, 2, 10, f'[ICE BLADE] {damage} damage', 0, enemy_damage

    def bullet(self):
        damage = int(self.player_damage * 1.0) - self.enemy_defense
        return damage, 1, 1, f'[BULLET] {damage} damage'
    
    def spirit_will(self):
        damage = int(self.player_health/5 + self.player_damage/2) - self.enemy_defense
        return damage, 1, 4, f'[SPIRIT WILL] {damage} damage'
    
    def laser(self):
        damage = int(self.player_damage * 2.0) - self.enemy_defense
        return damage, 0, 10, f'[LASER] {damage} damage'
    
class Epic(Spells):
    def invisible_cut(self):
        damage = int(self.player_damage * 2.5) - int(self.enemy_defense/2)
        return damage, 1, 7, f'[INVISIBLE CUT] {damage} damage'

    def inferno(self):
        damage = int(self.player_damage * 4.0) - self.enemy_defense
        return damage, 2, 12, f'[INFERNO] {damage} damage'
     
    def recursion(self):
        global rec_counter
        damage = int(self.player_damage * rec_counter) - self.enemy_defense
        if rec_counter < 5:
            rec_counter += 0.2
        else:
            rec_counter = 5
        return damage, 2, 4, f'[RECURSION] {damage} damage'

    def inner_power(self):
        defense = self.player_defense + 1
        damage = self.player_damage + 1
        return damage, 2, 10, f'[INNER POWER] stats increased by 1', defense
    
    def meteor(self):
        damage = int(self.player_damage * 3.0) - self.enemy_defense
        return damage, 1, 5, f'[METEOR] {damage} damage'
    
    def implosion(self):
        damage = int(self.player_damage * 3.5) - int(self.enemy_defense/2)
        return damage, 2, 10, f'[IMPLOSION] {damage} damage'
    
    def temporal_bolt(self):
        global tb_counter
        damage = int(self.player_damage * 2.0) - self.enemy_defense
        if tb_counter > 1:
            tb_counter -= 1
        return damage, 1, tb_counter, f'[TEMPORAL BOLT] {damage} damage'	
    
    def fracture(self):
        damage = int(self.player_damage * 3.0) - self.enemy_defense
        defense = self.enemy_defense - 2
        if defense < 0:
            defense = 0
        return damage, 2, 7, f'[FRACTURE] {damage} damage', defense

    def Typhoon(self):
        damage = int(self.player_damage * 3.0) - self.enemy_defense
        enemy_damage = self.enemy_damage - 2
        if enemy_damage < 1:
            enemy_damage = 1
        return damage, 2, 7, f'[TYPHOON] {damage} damage', 0, enemy_damage

    def temporal_reflexion(self):
        damage = int(self.enemy_damage * 1.0) - self.enemy_defense
        return damage, 2, 8, f'[TEMPORAL REFLEXION] {damage} damage'
    
    def weakening_curse(self):
        defense = self.enemy_defense - 4
        damage = self.enemy_damage - 4
        if defense < 0 :
            defense = 0
        if damage < 1:
            damage = 1
        return 0, 2, 10, f'[WEAKENING CURSE] stats decreased by 4', defense, damage
    
    def chaos_magic(self):
        rand = (randrange(1,35) / 10)
        damage = int(self.player_damage * rand) - self.enemy_defense
        return damage, 1, 4, f'[CHAOS MAGIC] {damage} damage'
    
    def syphon(self):
        damage = int(self.player_damage * 2.5) - self.enemy_defense
        if damage < 1:
            return damage, 1, 10, f'[SYPHON] {damage}', 0
        return damage, 1, 10, f'[SYPHON] {damage} damage | recovered {damage} HP'
    
class Legendary(Spells):
    def soul_pierce(self):
        damage = int(self.player_damage * 2.5)
        return damage, 1, 5, f'[SOUL PIERCE] {damage} damage'

    def spirit_cutter(self):
        damage = int(self.player_health/20 * self.player_damage) - self.enemy_defense
        return damage, 1, 4, f'[LIGHT CUTTER] {damage} damage'
     
    def stormbreak(self):
        global rec_counter
        damage = int((self.player_damage + self.player_defense) * 2.0) - self.enemy_defense
        return damage, 2, 8, f'[STORMBREAK] {damage} damage'
    
    def Hex(self):
        damage = int(self.player_damage * 2.5) - self.enemy_defense
        defense = self.enemy_defense - 2
        enemy_damage = self.enemy_damage - 2
        if defense < 0 :
            defense = 0
        if enemy_damage < 1:
            enemy_damage = 1
        return damage, 1, 10, f'[HEX] {damage} damage | stats decreased by 2', defense, enemy_damage
    
    def heaven_annihilation(self):
        damage = int(self.player_damage * 10) - self.enemy_defense
        return damage, 2, 25, f'[HEAVEN ANNIHILATION] {damage} damage'
    
    def divide(self):
        damage = int(self.enemy_health/2)
        return damage, 2, 20, f'[DIVIDE] the enemy health has been divided!'
    
    def evolve(self):
        defense = self.player_defense + 2
        damage = self.player_damage + 2
        return damage, 2, 15, f'[EVOLVE] stats increased by 2', defense
    
    def wheel_of_fate(self):
        #FUNCTION NOT USED (DECORATIVE)
        #ID -> 0
        pass	
    
    def ascencion(self):
        global ascended
        if ascended == False:
            ascended = True
            return 'ascension',  2, 20, f'[ASCENSION] stats increased by 1', 1
        else:
            return 'ascension', 0, 0, f'The spell failed', 0 

    def reversal(self):
        temp = self.enemy_health
        self.enemy_health = self.player_health
        self.player_health = temp
        return self.player_health, 2, 20, f'[REVERSAL] you and the enemy changed souls', self.enemy_health

    def blood_magic(self):
        damage = int(self.player_damage * (100 / self.player_health))
        damage = int(max(damage, self.player_damage * 1.0))  
        return damage, 1, 5, f'[BLOOD MAGIC] {damage} damage'
    
    def even_odd(self):
        rand = (randrange(20,50) / 10)
        damage = int(self.player_damage * rand) - self.enemy_defense
        return damage, 1, 5, f'[EVEN ODD] {damage} damage'
    
    def death(self):
        damage = self.enemy_health
        return damage, 2, 60, f'[DEATH] INSTADEATH!'
    
    def gate_opener(self):
        global opened
        if opened == False:
            opened = True
            return 'GATE', 3, 0, f'A GATE HAS OPENED, SOMETHING IS OFF...', 50
        else:
            return 'GATE', 3, 0, f'[GATE] Recovered 20 ap... how?',20
        