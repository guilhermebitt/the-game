from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty, NumericProperty, BooleanProperty
from kivy.core.window import Window
from items import Equipament

# Settings
Builder.load_file('widgets/playerstats.kv')
Builder.load_file('widgets/enemystats.kv')
Builder.load_file('widgets/actionbuttons.kv')
Builder.load_file('widgets/optionbuttons.kv')
Builder.load_file('widgets/customwidgets.kv')
Builder.load_file('widgets/inventory.kv')

class PlayerStats(GridLayout):
    pass


class EnemyStats(BoxLayout):
    pass


class InvOptions(Widget):
    visible = BooleanProperty(False)
    is_spell = BooleanProperty(False)
    size_hint = None, None
    def __init__(self, **kwargs):
        super(InvOptions, self).__init__(**kwargs)
        self.pos = [10000, 10000]
        global TheApp
        TheApp = App.get_running_app()

    def call_options(self, x, y, instance):
        if not instance.source == 'assets/hud/slot.png':
            self.pos = [x-200, y]
            self.visible = True
            self.is_spell = instance.type[0] == 'spell'

    def hide(self):
        self.visible = True
        self.pos = [10000, 10000]
    
    def option_pressed(self):
        self.pos = [10000, 10000]
    
    def use(self):
        item_slot = self.parent.parent.ids.get(f'item{slot_id}')
        if item_slot.type[0] == 'spell':
            TheApp.root.get_screen('the').do_spell(item_slot.type[1])
    
    def info(self):
        item_slot = self.parent.parent.ids.get(f'item{slot_id}')
        the = self.parent.parent.parent.parent.parent.parent
        if the.turn == 'Player':
            if item_slot.type[0] == 'spell':
                try:
                    the.phrase(item_slot.type[2])
                    the.phrase(f'Type of damage: [color=fcba03]{item_slot.type[3]}[/color].')
                except:
                    the.phrase('No description found.')
            else:
                try:
                    the.phrase(item_slot.type[2])
                except:
                    the.phrase('No description found.')

    def discart(self):
        item_slot = self.parent.parent.ids.get(f'item{slot_id}')
        the = self.parent.parent.parent.parent.parent.parent
        if item_slot.type[0] != 'spells':
            item = Equipament(item_slot.type[0], item_slot.type[1]).get
            the.verify_item_stats(item, reverse=True)
            the.update_player()
        TheApp.root.get_screen('the').update_inventory(slot_id)


class ItemSlot(ButtonBehavior, Image):
    type = ListProperty()
    slot_id = NumericProperty()
    def __init__(self, **kwargs):
        super(ItemSlot, self).__init__(**kwargs)
        self.size_hint = None, None
        self.fit_mode = 'fill'
        self.source = 'assets/hud/slot.png'
    
    def on_release(self):
        global slot_id
        slot_id = self.slot_id

        mouse_x, mouse_y = Window.mouse_pos
        self.parent.parent.parent.ids.menu.call_options(mouse_x, mouse_y, self)


class Inventory(BoxLayout):
    def __init__(self, **kwargs):
        super(Inventory, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)
    
    def on_mouse_pos(self, *args):
        pass


class Game(Widget):
    def on_touch_down(self, touch):
        if self.ids.inv.ids.menu.visible:
            self.ids.inv.ids.menu.hide()
        return super(Game, self).on_touch_down(touch)


class CutScene(Widget):
    pass


class Menu(Widget):
    pass


class Options(Widget):
    pass


class Death(Widget):
    pass
