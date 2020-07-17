from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

kv = '''
<SettingsScreen>:
    MDFloatLayout:
        MDLabel:
            text: "Pantalla de Ajustes"
            font_style: "H2"
'''

class SettingsScreen(MDScreen):
    Builder.load_string(kv)