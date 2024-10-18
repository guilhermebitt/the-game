# COLLAPSE ALL: CONTROL + K + CONTROL + 0
# COLLAPSE CLASSES: CONTROL + K + CONTROL + 1
# COLLAPSE METHODS: CONTROL + K + CONTROL + 2
# UNCOLLAPSE ALL: CONTROL+ K + CONTROL + J

import sys
sys.path.append('widgets')
sys.path.append('screens')
import WidgetsPy, ScreensPy
from ScreensPy import MyScreens, MenuScreen, GameScreen, MainScreenManager, CutSceneScreen
from WidgetsPy import Inventory
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import NoTransition
from kivy.clock import Clock
from random import randrange
from spells import Spells, Category
from enemies import Enemy
from items import Equipament
import enemies

# Settings
Window.size = 1280, 720
Window.minimum_width = 1280
Window.minimum_height = 720
ascension = False


class Player(GameScreen):
    def player_stats(self):
        self.p_stats = self.game.ids.p_stats.ids
        self.p_life = self.p_stats.life_bar  # PLAYER LIFE
        self.p_life_lbl = self.p_stats.life_txt  # PLAYER LIFE
        self.p_deff = self.p_stats.deff_lbl  # PLAYER DEFENSE
        self.p_atk = self.p_stats.atk_lbl  # PLAYER ATTACK
        self.p_moves = self.p_stats.moves  # PLAYER MOVEMENTS
        self.ap = self.p_stats.ap_bar  # ACTION POINTS BAR
        self.ap_lbl = self.p_stats.ap_txt  # ACTION POINTS LABEL
        self.coin = self.p_stats.coin  # PLAYER MONEY

    def update_player(self):
        self.p_life.value += self.life_increase
        self.p_life.max += self.max_life_increase
        self.p_life_lbl.text = f'{int(self.p_life.value)}/{int(self.p_life.max)}'
        self.ap.value += self.ap_increase
        self.ap.max += self.max_ap_increase
        self.ap_lbl.text = f'{int(self.ap.value)}/{int(self.ap.max)}'
        self.p_deff.text = str(int(self.p_deff.text) + self.deff_increase)
        self.p_atk.text = str(int(self.p_atk.text) + self.atk_increase)
        self.p_moves.text = str(int(self.p_moves.text) + self.moves_increase)

        self.life_increase = 0
        self.max_life_increase = 0
        self.ap_increase = 0
        self.max_ap_increase = 0
        self.deff_increase = 0
        self.atk_increase = 0
        self.moves_increase = 0

    def endturn(self):
        if self.turn == 'Player' and self.prompt_state == 0:
            self.turn = 'Enemy'
            self.phrase('[color=fcba03]You ended your turn.[/color]')
            self.enemys_turn_trig(0.5)
    
    def _reduce_ap(self, amount):
        self.ap.value -= amount
        max = self.ap_lbl.text[self.ap_lbl.text.find('/'):]
        self.ap_lbl.text = f'{int(self.ap.value)}{max}'
        if self.ap.value == 0:
            self.died = True
            self.phrase_queue = []
            self.phrase('[color=ba0b0b]You feel your soul leaving your body, good try Mr. President...[/color]')
            self.die_trig()
            self.phrase_queue = []
            self.turn = 'Death'
    
    def _reduce_moves(self, amount):
        self.p_moves.text = str(int(self.p_moves.text) - amount)
    
    def _reduce_life(self, amount):
        self.p_life.value -= amount
        max = self.p_life_lbl.text[self.p_life_lbl.text.find('/'):]
        self.p_life_lbl.text = f'{int(self.p_life.value)}{max}'
        if int(self.p_life_lbl.text[:self.p_life_lbl.text.find('/')]) == 0:
            self.died = True
            self.phrase_queue = []
            self.phrase('[color=ba0b0b]You feel your soul leaving your body, good try Mr. President...[/color]')
            self.die_trig()
            self.turn = 'Death'

    def attack(self):
        p_atk = int(self.p_atk.text)
        e_deff = int(self.e_deff.text)

        self.damage = p_atk - e_deff
        if self.damage < 0:
            self.damage = 0
        
        self._reduce_ap(2)
        self._reduce_moves(1)

        text = self.enemy.reduce_e_life(self.damage)
        if text != 'None':
            self.phrase(text)
        if int(self.e_life.value) < 0:
            self.e_life.value = '0'
        if text == 'None':
            self.phrase(f'You deal {self.damage} points of damage.')

        self.update_enemy()

    def cast(self, spell_id):
        global ascension
        attack = [self.p_atk.text, self.e_atk.text]
        defense = [self.p_deff.text, self.enemy.deff]
        health = [self.p_life.value, self.e_life.value]
        moves = int(self.p_moves.text)
        lack_of_moves = self.p_moves.text
        #spell_id = 25  # CHANGE THE SPELL MANUALLY BY USING THIS VARIABLE
        if spell_id == 0:
            spell_id = randrange(1,46)
        results = Spells(attack,defense,health,moves,spell_id).act

        self._reduce_moves(results[1])

        if int(self.p_moves.text) < 0:
            self.p_moves.text = lack_of_moves
            return self.phrase('Not enough moves to cast spell.')
        self._reduce_ap(results[2])
        self.phrase(results[3])
        if spell_id in Category.heal():
            self._reduce_life(results[0] * -1)
        if spell_id in Category.buff():
            self.p_atk.text = str(results[0])
            self.p_deff.text = str(results[4])
            self.update_enemy()
        if spell_id in Category.debuff_defense():
            self.enemy.deff = str(results[4])
        if spell_id in Category.debuff_attack():
            self.enemy.atk = str(results[5])
        if spell_id in Category.damage():
            text = self.enemy.reduce_e_life(results[0])
            if text != 'None':
                self.phrase(text)
        if  spell_id in Category.other():
            if  results[0] == 'ascension':
                ascension = True
            elif results[0] == 'GATE':
                self.ap.value += results[4]
            else:
                self.enemy.life = str(results[4])
                self._reduce_life(results[4] - results[0])

        self.update_enemy()


class The(Player):
    enemy = None
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        self.turn = 'Player'  # player starts with the turn
        self.life_increase = 0
        self.max_life_increase = 0
        self.ap_increase = 0
        self.max_ap_increase = 0
        self.deff_increase = 0
        self.atk_increase = 0
        self.moves_increase = 0
        self.coin_increase = 1
        self.ap_recover_increase = 1
        
    def on_enter(self, *args):
        self.player_stats()
        self.e_stats = self.game.ids.e_stats.ids
        if self.turn == 'Enemy':
            self.enemys_turn_trig(0.5)
        self.died = False

        self.e_life = self.e_stats.l_bar
        self.e_life_txt = self.e_stats.l_txt
        self.e_atk = self.e_stats.atk
        self.e_deff = self.e_stats.deff
        self.e_name = self.e_stats.name
        self.e_img = self.e_stats.img

        if not self.events.text:
            self.terminal_text = '[color=fcba03]Welcome[/color], you need to save our planet againist [color=fcba03]they[/color]!'
            self.phrase(self.terminal_text)
        else:
            self.terminal_text = self.events.text
            self.events.text = ''
            self.write(self.terminal_text)

        if not self.enemy:
            self.current_enemy = 1
            self.spawn_enemy()
            self.update_enemy()

        if GameScreen.sound:
            GameScreen.sound.play()
            pass
        self.inventory = {'1': 'assets/hud/slot.png', '2': 'assets/hud/slot.png', '3': 'assets/hud/slot.png', '4': 'assets/hud/slot.png', '5': 'assets/hud/slot.png', '6': 'assets/hud/slot.png', '7': 'assets/hud/slot.png', '8': 'assets/hud/slot.png', '9': 'assets/hud/slot.png', '10': 'assets/hud/slot.png'}
        self.update_inventory()
        heal = Spells(id=3).act
        description = heal[-1]
        damage_type = heal[-2]
        self.insert_inventory(f'assets/spells/heal.png', ['spell', 3, description, damage_type])
    
    def insert_inventory(self, source, type):
        for chave in self.inventory:
            item_slot = self.game.ids.inv.ids.get(f'item{chave}')
            if item_slot.source == 'assets/hud/slot.png':
                self.update_inventory(chave, source, type)
                if not item_slot.texture:
                    item_slot.source = 'assets/hud/placeholder.png'
                break
    
    def update_inventory(self, slot=0, source='assets/hud/slot.png', type=['None', None, 'None'],):
        if slot == 0:
            for chave in self.inventory:
                item_slot = self.game.ids.inv.ids.get(f'item{chave}')
                item_slot.source = self.inventory[chave]
                item_slot.type = ['None', None, 'None']
        else:
            item_slot = self.game.ids.inv.ids.get(f'item{slot}')
            item_slot.source = source
            item_slot.type = type

    def stop_music(self):
        if self.sound:
            self.sound.stop()
    
    def start_menu_music(self):
        if self.sound:
            MenuScreen.sound.play()

    def back_to_menu(self):
        if self.died == False:
            self.manager.current = 'menu'
            self.stop_music()
            self.start_menu_music()

    def mute(self):
        if GameScreen.sound.volume != 0:
            self.last_volume = GameScreen.sound.volume
            MyScreens.change_volume(GameScreen, 0)
        elif GameScreen.sound.volume == 0:
            try:
                MyScreens.change_volume(GameScreen, self.last_volume)
            except:
                MyScreens.change_volume(GameScreen, 0.1)

    def spawn_enemy(self):
        self.id = self.current_enemy
        self.enemy = enemies.Enemy(self.id, int(self.p_deff.text)).choose()
        self.e_turns = self.enemy.turns
        self.e_max_l = self.enemy.life
        if self.enemy.entry_phrase != 'None':
            self.phrase(self.enemy.entry_phrase)
        self.current_enemy += 1

    def update_enemy(self):
        self.e_atk.text = self.enemy.atk
        self.e_deff.text = self.enemy.deff
        self.e_name.text = self.enemy.name
        self.e_img.source = self.enemy.img
        self.enemy.p_deff = int(self.p_deff.text)
        # ENEMYS LIFE
        self.e_life.max = int(self.e_max_l)
        self.e_life_txt.text = f'{self.enemy.life}/{self.e_max_l}'
        self.e_life.value = int(self.enemy.life)
        self._check_if_the_enemy_is_dead()

    def _check_if_the_enemy_is_dead(self):
        if int(self.e_stats.l_bar.value) <= 0:
            self.phrase('Enemy defeated!')
            self.generate_money = True
            self.generate_spell = True
            self.generate_item = True
            self.generate_loot(self.id)
            try:
                self.spawn_enemy()
                self.update_enemy()
            except:
                self.current_enemy -= 1
                self.spawn_enemy()
                self.update_enemy()

    def verify_if_repete(self, source):
        res = False
        for chave in self.inventory:
            item_slot = self.game.ids.inv.ids.get(f'item{chave}')
            if item_slot.source == source:
                res = True
        return res
    
    def is_full(self):
        res = True
        for chave in self.inventory:
            item_slot = self.game.ids.inv.ids.get(f'item{chave}')
            if item_slot.source == 'assets/hud/slot.png':
                res = False
        return res

    def generate_loot(self, enemy_id):
        self.enemy = enemies.Enemy(enemy_id, int(self.p_deff.text)).choose()
        loot = self.enemy.loot
        for chave in loot:
            

            if chave == 'money' and self.generate_money == True:
                self.coin.text = str(int(self.coin.text) + (loot["money"] * self.coin_increase))
                self.phrase(f'You gained {loot["money"] * self.coin_increase} coins.')


            if self.is_full() == True:
                self.phrase("Your inventory is full, you can't carry any loot!")
                return None


            if chave == 'spell' and self.generate_spell == True:
                spell = Spells(id=loot[chave]).act
                full_spell_name = spell[3]
                description = spell[-1]
                damage_type = spell[-2]
                spell_name = full_spell_name[full_spell_name.find('[')+1:full_spell_name.find(']')].lower()
                source = f'assets/spells/{spell_name}.png'
                if self.verify_if_repete(source) == True:
                    self.generate_money = False
                    self.generate_spell = True
                    self.generate_item = False
                    self.generate_loot(enemy_id)
                    return None
                else:
                    self.generate_money = False
                    self.generate_spell = False
                    self.generate_item = True
                self.insert_inventory(source, ['spell', loot[chave], description, damage_type])
                self.phrase_queue.append(f'[color=#3ca832]You got a {spell_name.upper()}! see "info" in your turn for more details.[/color]')
            if self.is_full() == True:  # depois de adicionar a magia, verifica se o inventário encheu
                self.phrase("Your inventory is full, you can't carry any loot!")
                return None
            

            if chave == 'item' and self.generate_item == True:
                item = Equipament('random', loot[chave]).get  # Change manual looting by here
                item_name = item['name'].casefold().replace(' ', '_')
                description = self.verify_item_stats(item)
                source = f'assets/itens/{item_name}.png'
                if self.verify_if_repete(source) == True:
                    self.generate_money = False
                    self.generate_spell = False
                    self.generate_item = True
                    self.generate_loot(enemy_id)
                    return None
                self.insert_inventory(f'assets/itens/{item_name}.png', [item['category'], loot[chave], description])
                self.update_player()
                self.phrase_queue.append(f'[color=#3ca832]You got a {item["category"]}! see "info" in your turn for more details.[/color]')

    def verify_item_stats(self, item, reverse=False):
        if item['category'] == 'artifact':
            if reverse == False:
                self.max_life_increase = item['increase']
            else:
                self.max_life_increase -= item['increase']
            description = f'{item["name"]}: Increases max hp of the player by {item["increase"]} points.'

        elif item['category'] == 'weapon':
            if reverse == False:
                self.atk_increase = item['increase']
            else:
                self.atk_increase -= item['increase']
            description = f'{item["name"]}: Increases attack of the player by {item["increase"]} points.'

        elif item['category'] == 'armor':
            if reverse == False:
                self.deff_increase = item['increase']
            else:
                self.atk_increase -= item['increase']
            description = f'{item["name"]}: Increases defense of the player by {item["increase"]} points.'

        elif item['category'] == 'soul':
            if reverse == False:
                self.atk_increase = item['increase']
            else:
                self.deff_increase -= item['increase']
            description = f'{item["name"]}: Increases both attack and defense of the player by {item["increase"]} points.'
            
        elif item['category'] == 'potion':
            self.generate_potions(item, reverse)
            description = "Potions doesn't have descriptions yet."
        return description
    
    def generate_potions(self, item, reverse=False):
        stats = item['stat'].split()
        for stat in stats:
            if stat[0] == '+':
                if reverse == False:
                    what_to_do = 'increase'
                else:
                    what_to_do = 'decrease'
            else:
                if reverse == False:
                    what_to_do = 'decrease'
                else:
                    what_to_do = 'increase'

            match stat[1:]:
                case 'defense':
                    if what_to_do == 'increase':
                        self.deff_increase = item['increase']
                    else:
                        self.deff_increase -= item['increase']
                case 'attack':
                    if what_to_do == 'increase':
                        self.atk_increase = item['increase']
                    else:
                        self.atk_increase -= item['increase']
                case 'money':
                    if what_to_do == 'increase':
                        self.coin_increase = item['increase']
                    else:
                        self.coin_increase -= item['increase']
                        if self.coin_increase == 0:
                            self.coin_increase = 1
                case 'heal':
                    if what_to_do == 'increase':
                        self.life_increase = item['increase']
                    else:
                        self.life_increase -= item['increase']
                case 'ap recover':
                    if what_to_do == 'increase':
                        self.ap_recover_increase = item['increase']
                    else:
                        self.ap_recover_increase -= item['increase']
                        if self.ap_recover_increase == 0:
                            self.ap_recover_increase = 1

    def enemys_turn(self, dt):
        if self.died == False and (self.manager and self.manager.current == 'the'):
            action = self.enemy.do_action()
            if action[1] == 'attack':
                self.phrase(action[0][1])
                self._reduce_life(action[0][0])
            elif action[1] == 'dialogue':
                self.phrase(action[0])
            self.enemy.turns -= 1
            self.update_enemy()
            if self.enemy.turns > 0:
                self.enemys_turn_trig()
            else:
                self.players_turn_trig()

    def players_turn(self, dt):
        if self.died == False:
            self.phrase("[color=fcba03]It's your turn.[/color]")
            self.turn = 'Player'
            if ascension == True:
                self.p_moves.text = '3'
            else:
                self.p_moves.text = '2'
            self.enemy.turns = self.e_turns

    def do_attack(self):
        if self.turn == 'Player' and self.prompt_state == 0:
            if int(self.p_moves.text) <= 0:
                return
            self.attack()

    def do_spell(self, spell_id):
        if self.turn == 'Player' and self.prompt_state == 0:
            if int(self.p_moves.text) <= 0:
                return
            self.cast(spell_id)

    def die(self, dt, died=False, button=False):
        self.phrase_queue = []
        if button == True and self.died == True:
            return
        elif died == True or self.died == True:
            self.stop_music()
            self.manager.current = 'death'

 
class TheApp(App):
    def build(self) -> None:
        Window.clearcolor = 0.20, 0.20, 0.15, 1
        self.screen_manager = MainScreenManager(transition=NoTransition())
        return self.screen_manager

    def restart_game(self):
        self.screen_manager.remove_widget(self.screen_manager.get_screen('the'))
        self.screen_manager.add_widget(The(name='the'))
        self.screen_manager.current = 'the'

    def quit(self):
        App.get_running_app().stop()
    
    def click(self):
        MyScreens.click(MyScreens)

    def start_cutscene(self):
        pass


if __name__ == '__main__':
    TheApp().run()
