from kivymd.uix.list import OneLineIconListItem, IconLeftWidget
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout


class ListIcon(OneLineIconListItem):
    def __init__(self, **kw):
        super().__init__()
        self.text = kw["text"]
        self.icon = IconLeftWidget(icon=kw["icon"])
        self.add_widget(self.icon)
        self.on_release = kw["on_release"]


def loading_message():
    cargando_mensaje = MDBoxLayout(orientation="vertical")
    cargando_mensaje.add_widget(MDLabel(text="CARGANDO", halign="center", font_size="300sp",
                                        font_style="H5"))
    for i in range(3):
        cargando_mensaje.add_widget(MDLabel(font_size="300sp",
                                            font_style="H1"))

    return cargando_mensaje

def no_trips_message():
    nt_message = MDBoxLayout(orientation="vertical")
    nt_message.add_widget(MDLabel(font_size="300sp", font_style="H1"))
    nt_message.add_widget(MDLabel(text="NO HAY VIAJES PUBLICADOS", halign="center", font_size="300sp",
                                font_style="H3"))
    for i in range(3):
        nt_message.add_widget(MDLabel(font_size="300sp", font_style="H1"))

    return nt_message