from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.app import MDApp

kv = '''
<SettingsScreen>:
    MDFloatLayout:
        MDLabel:
            text: "Pantalla de Ajustes"
            font_style: "H2"
'''

class SettingsScreen(MDScreen):
    Builder.load_string(kv)
    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()

    def on_pre_enter(self, *args):
        self.app.root.current_screen.ids.tool_bar.right_action_items = []