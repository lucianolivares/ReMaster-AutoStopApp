from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from startup_screen import StartupScreen


class AutoStop(MDApp):
    def build(self):
        Window.size = (480, 720)
        sm = ScreenManager()
        self.title = "AutoStop"
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        return sm

    def on_start(self):
        ss = StartupScreen()
        self.root.add_widget(ss)
        self.root.current = "startup_screen"

AutoStop().run()
