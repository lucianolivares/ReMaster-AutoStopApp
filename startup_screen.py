from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from login_screen import LoginScreen
from myfirebase import exchange_refresh_token

Builder.load_string("""
<StartupScreen>
    name: "startup_screen"
    md_bg_color: app.theme_cls.primary_color

    Image:
        source: "resources/icono.png"
        size_hint: (.2, .2)
        pos_hint: {'center_x': .5, 'center_y':.5}
        
""")

APP = MDApp.get_running_app()

class StartupScreen(MDScreen):
    """[summary]
    StartupScreen is to start the application with the logo of the application
    and here it checks if there is a registered session and in that case, it loads
    the navigation_screen screen and on the contrary redirects you to the login_screen
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        try:
            # Try to read the persisten signing credentials (refresh token)
            # Use refresh token to get a new idToken
            exchange_refresh_token()
        except:
            Clock.schedule_once(lambda dt: self.load_login_screen(), 2)

    def load_login_screen(self):
        login_screen = LoginScreen()
        APP.root.add_widget(login_screen)
        APP.root.current = "login_screen"
        self.remove_screen()
    
    def remove_screen(self):
        current = APP.root.get_screen("startup_screen")
        APP.root.remove_widget(current)
