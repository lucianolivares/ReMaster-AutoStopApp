from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

kv = '''
<PassengersAvailableScreen>:
    MDFloatLayout:
        MDLabel:
            text: "Pasajeros Disponibles"
            font_style: "H2"
'''

class PassengersAvailableScreen(MDScreen):
    Builder.load_string(kv)