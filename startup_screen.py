from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from login_screen import LoginScreen
from myfirebase import Login
from navigation_screen import NavigationScreen

Builder.load_string("""
<StartupScreen>
    name: "startup_screen"
    md_bg_color: app.theme_cls.primary_color

    Image:
        source: "resources/icons/icono.png"
        size_hint: (.2, .2)
        pos_hint: {'center_x': .5, 'center_y':.5}
        
""")

class StartupScreen(MDScreen):
    """[summary]
    StartupScreen is to start the application with the logo of the application
    and here it checks if there is a registered session and in that case, it loads
    the navigation_screen screen and on the contrary redirects you to the login_screen
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = MDApp.get_running_app()
        self.login = Login()

    def on_pre_enter(self, *args):
        try:
            # Try to read the persisten signing credentials (refresh token)
            # Use refresh token to get a new idToken
            self.login.exchange_refresh_token()
            Clock.schedule_once(lambda dt: self.load_navigation_screen(), 1)
        except:
            Clock.schedule_once(lambda dt: self.load_login_screen(), 1)

    def load_navigation_screen(self):
        nav_screen = NavigationScreen()
        self.app.root.add_widget(nav_screen)
        self.app.root.current = "navigation_screen"

    def load_login_screen(self):
        login_screen = LoginScreen()
        self.app.root.add_widget(login_screen)
        self.app.root.current = "login_screen"
