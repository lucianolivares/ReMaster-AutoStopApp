from kivy.clock import Clock
from kivy.lang import Builder
from kivy.network.urlrequest import UrlRequest
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.clock import mainthread

from add_trip_layout import AddTripLayout
from myfirebase import Database
from trips_banner import TripsBanner
from classes import *


Builder.load_string('''
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


class TripsAvailableScreen(MDScreen):

    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.add_trip_dialog = None
        self.content = None
        self.hint_text_seats = "Asientos Disponibles"
        # Data
        self.city_from = None
        self.city_to = None
        self.hour = None
        self.n_passenger = int
        
    def on_pre_enter(self, *args):
        if not "driver" in APP.data:
            self.add_trip_button.disabled = True
        self.add_trip_button.bind(on_release=self.show_add_trip_dialog)
        # Charge Trips
        self.trips_available()

    def trips_available(self):
        url = f'https://remasterautostop-fc4ec.firebaseio.com/trips_available.json'
        get_request = UrlRequest(url, verify=False, on_success=self.load_data)

    def load_data(self, request, result):
        trips_data = result
        self.ids.trips_grid.clear_widgets()
        self.refresh_available_trips(trips_data)

    def refresh_available_trips(self, trips_data):
        try :
            for trip, data in trips_data.items():
                self.ids.trips_grid.add_widget(TripsBanner(
                    kind_dialog="Trip",
                    city_from=data['city_from'],
                    city_to=data['city_to'],
                    name=data['driver'],
                    plate=data['plate'],
                    cel_number=data['cel_number'],
                    date=data['date'],
                    hour=data['hour'],
                    seats=f"{data['seats_available']} Disponibles",
                    trip_id=trip,
                    hint_text_seats=self.hint_text_seats,
                    reload_data=self.trips_available
                ))
        except :
            temp = no_trips_message()
            self.ids.trips_grid.add_widget(temp)

    def refresh_callback(self, *args):
        '''A method that updates the state of your application
        while the spinner remains on the screen.'''
        def refresh_callback(interval):
            self.ids.refresh_layout.refresh_done()

        self.trips_available()
        Clock.schedule_once(refresh_callback, 1.5)

    def show_add_trip_dialog(self, instance_button):
        """[summary]
        Function in charge of initializing a pop-up window in which
        we can enter a new trip available
        """
        if not self.add_trip_dialog:
            self.add_trip_dialog = MDDialog(
                size_hint=(.8, .7),
                title="Añadir Viaje:",
                type="custom",
                content_cls=AddTripLayout(seats=self.hint_text_seats),
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

    def add_trip(self, button):
        """[summary]
        Collect the data and run the method in myfirebase that creates a new 
        trip in the cloud
        """
        self.city_from = self.content.ids.city_from.text
        self.city_to = self.content.ids.city_to.text
        self.date = self.content.ids.date_label.text
        self.hour = self.content.ids.hour_label.text
        self.seats_available = self.content.ids.seats.text

        if (self.city_from and self.city_to and self.seats_available != "" and
            self.date != "Fecha" and self.hour != "Hora"):
            # If All fields are completed the add the Trip
            DATABASE.create_new_trip(
                APP.data['name'], APP.data['last_name'],
                self.city_from, self.city_to, self.date, self.hour,
                self.seats_available, APP.data['cel_number'], APP.data['driver']['plate']
            )

            self.close_dialog("")
            self.trips_available()

        else:
            print("Debes Completar Todos Los Datos")
        
    def close_dialog(self, button):
        """[summary]
        close and delete the add trip dialog
        """
        self.add_trip_dialog.dismiss()
        self.add_trip_dialog = None 
