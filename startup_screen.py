from kivymd.uix.screen import MDScreen
from kivy.lang import Builder



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



