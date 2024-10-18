from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from kivy.animation import Animation

# Settings
Builder.load_file('screens/game.kv')
Builder.load_file('screens/cutscene.kv')
Builder.load_file('screens/menu.kv')
Builder.load_file('screens/options.kv')
Builder.load_file('screens/death.kv')
Builder.load_file('screens/screens.kv')

class MainScreenManager(ScreenManager):
    pass


class MyScreens(Screen):
    button_click = None

    def __init__(self, **kwargs):
        super(MyScreens, self).__init__(**kwargs)
        if not MyScreens.button_click:
            MyScreens.button_click = SoundLoader.load('sounds/button_click.wav')

    #def on_kv_post(self, base_widget):
    #    self.sound.volume = 0.1

    def click(self):
        if self.button_click:
            self.button_click.volume = 1
            self.button_click.play()

    def change_volume(self, value):
        if not self.sound:
            GameScreen.sound = SoundLoader.load('sounds/super_mario_main_theme.wav')  # temporary!
            self.sound.volume = 0.1
            self.sound.loop = True
        self.sound.volume = value


class MenuScreen(MyScreens):
    sound = None
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        if not MenuScreen.sound:
            MenuScreen.sound = SoundLoader.load('sounds/super_mario_main_theme.wav')  # I changed this sound to put on github
            self.sound.volume = 0.1
            self.sound.loop = True

    def on_kv_post(self, base_widget):
        if self.sound:
            self.sound.play()
            pass

    def change_menu(self):
        if self.sound:
            self.sound.stop()


class OptionsScreen(MyScreens):
    sound = None
    def on_kv_post(self, base_widget):
        if not GameScreen.sound:
            GameScreen.sound = SoundLoader.load('sounds/super_mario_main_theme.wav')  # temporary!
            self.sound.volume = 0.1
            self.sound.loop = True


class DeathScreen(MyScreens):
    death_sound = None
    sound = None
    def __init__(self, **kwargs):
        super(DeathScreen, self).__init__(**kwargs)
        if not DeathScreen.death_sound:
            DeathScreen.death_sound = SoundLoader.load('sounds/death_sound.wav')
    
    def on_enter(self):
        if self.death_sound:
            self.death_sound.play()
            pass

    def on_leave(self):
        if self.death_sound:
            self.death_sound.stop()
            pass
    
    def start_menu_music(self):
        MenuScreen.sound.play()


class CutSceneScreen(MyScreens):
    f_scene_music = None
    def __init__(self, **kwargs):
        super(CutSceneScreen, self).__init__(**kwargs)
        if not CutSceneScreen.f_scene_music:
            CutSceneScreen.f_scene_music = SoundLoader.load('sounds/super_mario_main_theme.wav')  # I changed this sound to put on github
            self.f_scene_music.volume = 0.1
            self.f_scene_music.loop = True


    def on_kv_post(self, base_widget):
        self.scene = self.ids.cutscene.ids
        self.cutscened = False

    def on_enter(self):
        self.scene.s1.pos = 3000, 3000
        self.scene.s2.pos = 3000, 3000
        self.scene.s3.pos = 3000, 3000
        if self.cutscened == False:
            if self.f_scene_music:
                self.f_scene_music.play()
            self.start_scene1()
        else:
            self.manager.current = 'the'
            if self.f_scene_music:
                self.f_scene_music.stop()
        
    def start_scene1(self):
        self.scene.s1.pos = 0, 0
        anim = Animation(x=-100, duration=0)  # Setting 0 secounds to skip this scene (I can't show it, it's personal)
        anim.start(self.scene.s1)
        anim.on_complete = self.start_scene2

    def start_scene2(self, widget):
        self.scene.s1.pos = 3000, 3000
        self.scene.s2.pos = -100, 0
        anim = Animation(x=0, duration=0)  # Setting 0 secounds to skip this scene (I can't show it, it's personal)
        anim.start(self.scene.s2)
        anim.on_complete = self.start_scene3
    
    def start_scene3(self, widget):
        self.scene.s2.pos = 3000, 3000
        self.scene.s3.pos = 0, 0
        anim = Animation(x=-100, duration=0)  # Setting 0 secounds to skip this scene (I can't show it, it's personal)
        anim.start(self.scene.s3)
        anim.on_complete = self.start_game_screen

    def start_game_screen(self, widget):
        self.scene.s3.pos = 3000, 3000
        self.manager.current = 'the'
        self.cutscened = True
        if self.f_scene_music:
            self.f_scene_music.stop()

class GameScreen(MyScreens):
    sound = None
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        if not GameScreen.sound:
            GameScreen.sound = SoundLoader.load('sounds/super_mario_main_theme.wav')
            self.sound.volume = 0.1
            self.sound.loop = True

    def on_enter(self):
        if self.sound:
            #self.sound.play()
            pass

    def on_kv_post(self, base_widget):
        self.game = self.ids.game
        self.events = self.game.ids.events
        self.e_area = self.game.ids.e_stats
        self.p_area = self.game.ids.player
        self.prompt_state = 0
        self.phrase_queue = []
        
        # CLOCK TRIGGERS
        self._update_phrase_trig = Clock.create_trigger(self._update_phrase, 0.015)
        self.enemys_turn_trig = Clock.create_trigger(self.enemys_turn, 1)
        self.players_turn_trig = Clock.create_trigger(self.players_turn, 1)
        self.die_trig = Clock.create_trigger(self.die, 5)

    def write(self, text):
        self.events.text = text

    def phrase(self, text):
        if self.prompt_state == 1:  # If the prompt is typing, append the text to a queue
            self.phrase_queue.append(text)
        else:
            self.text_phrase = text
            self.letter = ''
            self.index = 0
            self.prompt_state = 1  # defines the terminal to a 'typing' mode
            self.events.text = self.events.text + '| '  # Always put '>' in front of a phrase
            self._update_phrase_trig()
            log = open('log.txt','w')
            log.write(self.events.text)
    
    def _update_phrase(self, dt):
        if self.index < len(self.text_phrase):  # Verify if the phrase was another letters:
            self.letter = self.text_phrase[self.index]
            self.events.text = self.events.text + self.letter
            self.index += 1
            self._update_phrase_trig()
        else:
            self.prompt_state = 0
            self.events.text = self.events.text + '\n'
            if self.phrase_queue:  # Verify if there's another phrase in the queue
                next_phrase = self.phrase_queue.pop(0)  # Take the next phrase
                self.phrase(next_phrase)
