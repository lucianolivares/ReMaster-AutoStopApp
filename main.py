from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager


class AutoStop(MDApp):
    def build(self):
        sm = ScreenManager()
        return sm

AutoStop().run()