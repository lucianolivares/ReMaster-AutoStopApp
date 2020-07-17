from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

kv = '''
<TripsAvailableScreen>:
    MDFloatLayout:
        MDLabel:
            text: "Viajes Disponibles"
            font_style: "H2"
'''

class TripsAvailableScreen(MDScreen):
    Builder.load_string(kv)
