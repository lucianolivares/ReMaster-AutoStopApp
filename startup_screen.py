from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.lang import Builder
from myfirebase import MyFirebase
from kivy.clock import Clock

from navigation_screen import NavigationScreen
from signin_screen import SigninScreen


kv = """
<StartupScreen>
    name: "startup_screen"
    md_bg_color: app.theme_cls.primary_color
    Image:
        source: "resources/icons/icono.png"
        size_hint: (.2, .2)
        pos_hint: {'center_x': .5, 'center_y':.5}
        
"""

class StartupScreen(MDScreen):
    Builder.load_string(kv)
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()
        self.my_firebase = MyFirebase()
    
    def on_enter(self):
        nav_screen = NavigationScreen()
        signin_screen = SigninScreen()
        self.app.root.add_widget(nav_screen)
        self.app.root.add_widget(signin_screen)

        try:
            with open("refresh_token.txt", "r") as f:
                refresh_token = f.read()
                self.my_firebase.exchange_refresh_token(refresh_token)
                Clock.schedule_once(lambda dt: self.load_navigation(), 2)
        except:
            Clock.schedule_once(lambda dt: self.load_signin(), 2)
    
    def load_navigation(self):
        self.app.root.current = "navigation_screen"

    def load_signin(self):
        self.app.root.current = "signin_screen"


