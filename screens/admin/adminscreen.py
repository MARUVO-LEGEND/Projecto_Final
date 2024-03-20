from kivy.properties import ObjectProperty
from kivymd.uix.screen import MDScreen


class AdminScreen(MDScreen):
    hero_to = ObjectProperty(None)

    def move_to_screen_a(self):
        self.hero_to.start()




