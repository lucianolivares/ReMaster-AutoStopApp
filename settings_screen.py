from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.app import MDApp

Builder.load_string('''
<SettingsScreen>:
    MDRaisedButton:
        id: log_out_button
        text: "Cerrar Sesion"
        pos_hint: {"center_x": .5, "center_y": .2}
''')

APP = MDApp.get_running_app()

class SettingsScreen(MDScreen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.ids.log_out_button.bind(on_release=self.log_out)

    def on_pre_enter(self, *args):
        APP.root.current_screen.ids.tool_bar.right_action_items = []
    
    def log_out(self, instance):
        with open("resources/refresh_token.txt", "w") as f:
            f.write("")
            
        nav_screen = APP.root.current_screen

        from login_screen import LoginScreen
        self.login_screen = LoginScreen()
        APP.root.add_widget(self.login_screen)
        APP.root.current = "login_screen"
        
        APP.root.remove_widget(nav_screen)