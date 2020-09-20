from kivymd.uix.floatlayout import MDFloatLayout
from kivy.lang import Builder
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.app import MDApp

from myfirebase import Database
from add_trip_layout import AddTripLayout


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
        on_release: root.delete_trip()

    MDIconButton:
        id: edit_button
        icon: "pencil"
        pos_hint: {"center_x": .95, "center_y": .9}
        size_hint: (.15, .15)
        theme_text_color: "Custom"
        text_color: app.theme_cls.primary_color
        on_release: root.open_edit_dialog()

    MDIconButton:
        id: complete_button
        icon: "check"
        pos_hint: {"right": .975, "center_y": .1}
        size_hint: (.15, .15)
        theme_text_color: "Custom"
        text_color: (0,.9,.1,.9)
        user_font_size: "54sp"
        on_release: root.complete_trip()

""")

APP = MDApp.get_running_app()
DATABASE = Database()

class TripsBanner(MDFloatLayout):
    def __init__(self, plate="", **kw):
        super().__init__()
        self.kind_dialog = kw['kind_dialog']
        self.hint_text_seats = kw['hint_text_seats']
        self.trip_id = kw['trip_id']
        self.city_from = kw['city_from']
        self.city_to = kw['city_to']

        self.ids.title.text = f"{self.city_from} -> {self.city_to}"
        self.ids.name.text = kw['name']
        self.ids.plate.text = plate
        self.ids.cel_number.text = kw['cel_number']
        self.ids.hour.text = kw['hour']
        self.ids.date.text = kw['date']
        self.ids.seats.text = kw['seats']

        if plate == "":
            self.remove_widget(self.ids.plate)
    
    def open_edit_dialog(self):
        # Open Dialog
        self.edit_trip_dialog = MDDialog(
            size_hint=(.8, .7),
            title=f"Editar Viaje: {self.ids.title.text}",
            type="custom",
            content_cls=AddTripLayout(seats=self.hint_text_seats),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    text_color=APP.theme_cls.primary_color,
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="EDITAR", text_color=APP.theme_cls.primary_color,
                    on_release=self.edit_trip
                ),
            ],
        )

        self.content = self.edit_trip_dialog.ids.spacer_top_box.children[0]
        self.edit_trip_dialog.open()
        
    def close_dialog(self, button):
        self.edit_trip_dialog.dismiss()
        self.edit_trip_dialog = None 
    
    def edit_trip(self, button):
        self.city_from = self.content.ids.city_from.text
        self.city_to = self.content.ids.city_to.text
        self.date = self.content.ids.date_label.text
        self.hour = self.content.ids.hour_label.text
        self.seats = self.content.ids.seats.text

        if (self.city_from and self.city_to and self.seats != "" and
            self.date != "Fecha" and self.hour != "Hora"):
            # If All fields are completed the add the Trip
            update_kind = None
            if self.kind_dialog == "Request":
                update_kind = DATABASE.update_request
            else:
                update_kind = DATABASE.update_trip

            update_kind(self.trip_id, self.city_from, self.city_to, self.date, self.hour, self.seats)
            self.close_dialog("")
            #self.second_thread()
        
        else:
            print("Debes Completar Todos Los Datos")
    
    def complete_trip(self):
        if self.kind_dialog == "Request":
            DATABASE.complete_request(
                self.trip_id,
                self.ids.name.text,
                self.city_from,
                self.city_to,
                self.ids.date.text,
                self.ids.hour.text,
                self.ids.seats.text,
                self.ids.cel_number.text,
            )
            self.delete_trip()

        else:
            DATABASE.complete_trip(
                self.trip_id,
                self.ids.name.text,
                self.city_from,
                self.city_to,
                self.ids.date.text,
                self.ids.hour.text,
                self.ids.seats.text,
                self.ids.cel_number.text,
                self.ids.plate.text
            )
            self.delete_trip()

    def delete_trip(self):
        if self.kind_dialog == "Request":
            DATABASE.delete_passenger_request(self.trip_id)
        else:
            DATABASE.delete_trip(self.trip_id)
        #self.second_thread()