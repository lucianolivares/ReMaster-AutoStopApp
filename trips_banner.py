from kivymd.uix.floatlayout import MDFloatLayout
from kivy.lang import Builder


Builder.load_string("""
<TripsBanner>:
    canvas:
        Color:
            rgba: 0, .5, .8, 0.2
        RoundedRectangle:
            radius: (40, 40)
            pos: self.pos
            size: self.size
    
    MDLabel:
        id: title
        font_style: "H6"
        theme_text_color: "Primary"
        halign:"center"
        size_hint: (.8, .1)
        pos_hint: {"center_x": .5, "center_y": .9}

    OneLineIconListItem:
        id: name
        pos_hint: {"x": -0.05, "top": .8}
        size_hint: (.55, .2)
        font_style: "Body2"
        IconLeftWidget:
            icon: "account"

    OneLineIconListItem:
        id: cel_number
        pos_hint: {"x": -0.05, "top": .6}
        size_hint: (.55, .2)
        font_style: "Body2"
        IconLeftWidget:
            icon: "cellphone"

    OneLineIconListItem:
        id: plate
        pos_hint: {"x": -0.05, "top": .4}
        size_hint: (.55, .2)
        font_style: "Body2"
        IconLeftWidget:
            icon: "steering"
    
    OneLineIconListItem:
        id: hour
        pos_hint: {"x": .5, "top": .8}
        size_hint: (.5, .2)
        font_style: "Body2"
        IconLeftWidget:
            icon: "clock"

    OneLineIconListItem:
        id: date
        pos_hint: {"x": .5, "top": .6}
        size_hint: (.5, .2)
        font_style: "Body2"
        IconLeftWidget:
            icon: "calendar-check"
    
    OneLineIconListItem:
        id: seats
        pos_hint: {"x": .5, "top": .4}
        size_hint: (.5, .2)
        font_style: "Body2"
        IconLeftWidget:
            icon: "seat-recline-normal"
    
    MDIconButton:
        id: delete_button
        icon: "delete"
        pos_hint: {"center_x": .05, "center_y": .9}
        size_hint: (.15, .15)
        theme_text_color: "Error"

    MDIconButton:
        id: edit_button
        icon: "pencil"
        pos_hint: {"center_x": .95, "center_y": .9}
        size_hint: (.15, .15)
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color

    MDIconButton:
        id: complete_button
        icon: "check"
        pos_hint: {"right": .975, "center_y": .1}
        size_hint: (.15, .15)
        theme_text_color: "Custom"
        text_color: (0,.9,.1,.9)
        user_font_size: "54sp"

""")



class TripsBanner(MDFloatLayout):
    def __init__(self, plate="", **kw):
        super().__init__()

        self.trip_id = kw['trip_id']
        self.city_from = kw['city_from']
        self.city_to = kw['city_to']

        self.ids.title.text = f"{self.city_from} -> {self.city_to}"
        self.ids.driver.text = kw['driver']
        self.ids.plate.text = kw['plate']
        self.ids.cel_number.text = kw['cel_number']
        self.ids.hour.text = kw['hour']
        self.ids.date.text = kw['date']
        self.ids.seats.text = f"{kw['seats']} Disponibles"

        if plate == "":
            self.remove_widget(self.ids.plate)