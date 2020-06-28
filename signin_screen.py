from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

kv = """
<SigninScreen>
    name: "signin_screen"
    MDLabel:
        text: "Pantalla de Inicio de Sesion"
"""

class SigninScreen(MDScreen):
    Builder.load_string(kv)