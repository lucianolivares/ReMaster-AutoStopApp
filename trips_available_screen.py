from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDTimePicker, MDDatePicker
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivymd.uix.label import MDLabel

from trips_banner import TripsBanner
from myfirebase import Database

Builder.load_string('''
<AddTripDialog>
    orientation: "vertical"
    spacing: "8dp"
    size_hint_y: None
    height: "300dp"

    date_picker: date_picker

    MDTextField:
        id: city_from
        hint_text: "Desde"
        on_text_validate: city_to.focus = True

    MDTextField:
        id: city_to
        hint_text: "Para"
    
    MDBoxLayout:
        orientation: "horizontal"

        MDLabel:
            id: date_label
            size_hint_x: .9
            text: "Fecha"
            theme_text_color: "Secondary"
            
        MDIconButton:
            id: date_picker
            size_hint_x: .2
            icon: "calendar-edit"

    MDBoxLayout:
        orientation: "horizontal"
        
        MDLabel:
            id: hour_label
            size_hint_x: .9
            text: "Hora"
            theme_text_color: "Secondary"
            
        MDIconButton:
            id: hour_picker
            size_hint_x: .2
            icon: "clock"
    
    MDTextField:
        id: seats_available
        hint_text: "Asientos Disponibles"

<TripsAvailableScreen>:
    add_trip_button: add_trip_button
    
    MDScrollViewRefreshLayout:
        id: refresh_layout
        refresh_callback: root.refresh_callback
        root_layout: root

        MDGridLayout:
            id: trips_grid
            cols: 1
            padding: 10, 10
            spacing: 10, 10
            adaptive_height: True
            row_default_height: 650


    MDFloatingActionButton:
        id: add_trip_button
        icon: "plus"
        md_bg_color: app.theme_cls.primary_color
        pos_hint: {"center_x": .85, "center_y": .1}
'''
)


APP = MDApp.get_running_app()
DATABASE = Database()

class AddTripDialog(MDBoxLayout):
    def __init__(self, **kw):
        super().__init__()
        self.ids.hour_picker.on_release = kw["hour_picker"]
        self.date_picker.on_release = kw["date_picker"]


class TripsAvailableScreen(MDScreen):

    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.add_trip_dialog = None
        self.content = None
        # Data
        self.city_from = None
        self.city_to = None
        self.hour = None
        self.n_passenger = int
        # Charge Trips
        self.refresh_available_trips()

    def on_pre_enter(self, *args):
        self.add_trip_button.bind(on_release=self.show_add_trip_dialog)
        
    def refresh_available_trips(self):
        try :
            trips_data = DATABASE.trips_available("trips_available")
            for trip, data in trips_data.items():
                self.ids.trips_grid.add_widget(TripsBanner(
                    city_from=data['city_from'],
                    city_to=data['city_to'],
                    name=data['driver'],
                    plate=data['plate'],
                    cel_number=data['cel_number'],
                    date=data['date'],
                    hour=data['hour'],
                    seats=data['seats_available'],
                    trip_id=trip
                ))
        except :
            self.ids.trips_grid.add_widget(MDLabel(text="No hay Viajes Disponibles"))


    def refresh_callback(self, *args):
        def refresh_callback(interval):
            self.ids.trips_grid.clear_widgets()
            self.refresh_available_trips()
            self.ids.refresh_layout.refresh_done()

        Clock.schedule_once(refresh_callback, 1)

    def show_add_trip_dialog(self, instance_button):
        if not self.add_trip_dialog:
            self.add_trip_dialog = MDDialog(
                size_hint=(.8, .7),
                title="Añadir Viaje:",
                type="custom",
                content_cls=AddTripDialog(hour_picker=self.show_time_picker, date_picker=self.show_date_picker),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        text_color=APP.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="AÑADIR",
                        text_color=APP.theme_cls.primary_color,
                        on_release=self.add_trip
                    )
                ]
            )
        self.content = self.add_trip_dialog.ids.spacer_top_box.children[0]
        self.add_trip_dialog.open()

    def show_date_picker(self):
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.open()
    
    def get_date(self, date):
        self.content.ids.date_label.color = APP.theme_cls.primary_color
        self.content.ids.date_label.text = date.strftime("%d/%m/%Y")

    def show_time_picker(self):
        """Open time picker dialog."""
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self, instance, time):
        self.content.ids.hour_label.color = APP.theme_cls.primary_color
        self.content.ids.hour_label.text = time.strftime("%H:%M")

    def add_trip(self, button):
        self.city_from = self.content.ids.city_from.text
        self.city_to = self.content.ids.city_to.text
        self.date = self.content.ids.date_label.text
        self.hour = self.content.ids.hour_label.text
        self.seats_available = self.content.ids.seats_available.text

        if (self.city_from and self.city_to and self.seats_available != "" and
            self.date != "Fecha" and self.hour != "Hora"):
            # If All fields are completed the add the Trip
            DATABASE.create_new_trip(
                APP.data['name'], APP.data['last_name'],
                self.city_from, self.city_to, self.date, self.hour,
                self.seats_available, APP.data['cel_number'], APP.data['driver']['plate']
            )

            self.close_dialog("")

        else:
            print("Debes Completar Todos Los Datos")
        
    def close_dialog(self, button):
        self.add_trip_dialog.dismiss()
        self.add_trip_dialog = None 
