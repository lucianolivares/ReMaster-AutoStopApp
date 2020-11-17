from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivymd.app import MDApp


class AutoStop(MDApp):
    def build(self):
        """[summary]
        Constructor inicial de la aplicación
        Returns:
            [screenmanager]: [screenmanager principal de la aplicación]
        """
        #Window.size = (480, 720)
        sm = ScreenManager(transition=NoTransition())
        self.title = "AutoStop"
        self.WAK = ""
        self.theme_cls.primary_palette = "LightBlue"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.accent_palette = "Teal"
        self.theme_cls.theme_style = "Light"
        return sm

    def on_start(self):
        from startup_screen import StartupScreen
        ss = StartupScreen()
        self.root.add_widget(ss)
        self.root.current = "startup_screen"

AutoStop().run()
