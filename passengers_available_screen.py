from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.network.urlrequest import UrlRequest

from kivy.clock import Clock

from add_trip_layout import AddTripLayout
from trips_banner import TripsBanner
from myfirebase import Database
from classes import *


Builder.load_string('''
<PassengersAvailableScreen>:
    add_request_button: add_request_button

    MDScrollViewRefreshLayout:
        id: refresh_layout
        refresh_callback: root.refresh_callback
        root_layout: root

        MDGridLayout:
            id: passengers_grid
            cols: 1
            padding: 10, 10
            spacing: 10, 10
            adaptive_height: True
            row_default_height: 650


    MDFloatingActionButton:
        id: add_request_button
        icon: "plus"
        md_bg_color: app.theme_cls.primary_color
        pos_hint: {"center_x": .85, "center_y": .1}
'''
)

APP = MDApp.get_running_app()
DATABASE = Database()


class PassengersAvailableScreen(MDScreen):

    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.add_request_dialog = None
        self.content = None
        self.hint_text_seats = "Número de pasajeros"
        # Data
        self.city_from = None
        self.city_to = None
        self.hour = None
        self.n_passenger = int
        

    def on_pre_enter(self, *args):
        self.add_request_button.bind(on_release=self.show_add_request_dialog)
        # Charge Passengers Data
        self.trips_available()

    def trips_available(self):
        url = f'https://remasterautostop-fc4ec.firebaseio.com/passengers_request.json'
        get_request = UrlRequest(url, verify=False, on_success=self.load_data)

    def load_data(self, request, result):
        trips_data = result
        self.ids.passengers_grid.clear_widgets()
        self.refresh_available_passengers(trips_data)

    def refresh_available_passengers(self, trips_data):
        try:
            for passenger, data in trips_data.items():
                self.ids.passengers_grid.add_widget(TripsBanner(
                    kind_dialog="Request",
                    city_from=data['city_from'],
                    city_to=data['city_to'],
                    name=data['passenger'],
                    cel_number=data['cel_number'],
                    date=data['date'],
                    hour=data['hour'],
                    seats=f"{data['n_passengers']} Pasajeros",
                    trip_id=passenger,
                    hint_text_seats=self.hint_text_seats,
                    reload_data=self.trips_available
                ))
        except Exception as e:
            temp = no_trips_message()
            self.ids.passengers_grid.add_widget(temp)
    

    def refresh_callback(self, *args):
        '''A method that updates the state of your application
        while the spinner remains on the screen.'''
        def refresh_callback(interval):
            self.ids.refresh_layout.refresh_done()

        self.trips_available()
        Clock.schedule_once(refresh_callback, 1.5)

    def show_add_request_dialog(self, instance_button):
        """[summary]
        Function in charge of initializing a pop-up window in which 
        we can enter a new travel request
        """
        if not self.add_request_dialog:
            self.add_request_dialog = MDDialog(
                size_hint=(.8, .7),
                title="Añadir Solicitud:",
                type="custom",
                content_cls=AddTripLayout(seats=self.hint_text_seats),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        text_color=APP.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="AÑADIR", text_color=APP.theme_cls.primary_color,
                        on_release=self.add_request
                    ),
                ],
            )
        self.content = self.add_request_dialog.ids.spacer_top_box.children[0]
        self.add_request_dialog.open()

    def add_request(self, button):
        """[summary]
        Collect the data and run the method in myfirebase that creates a new 
        request in the cloud
        """
        self.city_from = self.content.ids.city_from.text
        self.city_to = self.content.ids.city_to.text
        self.date = self.content.ids.date_label.text
        self.hour = self.content.ids.hour_label.text
        self.n_passengers = self.content.ids.seats.text

        if (self.city_from and self.city_to and self.n_passengers != "" and
            self.date != "Fecha" and self.hour != "Hora"):
            # If All fields are completed the add the request
            DATABASE.add_passenger_request(
                APP.data['name'], APP.data['last_name'],
                self.city_from, self.city_to, self.date, self.hour,
                self.n_passengers, APP.data['cel_number']
            )
            self.close_dialog("")
            self.trips_available()
        else:
            print("Debes Completar Todos Los Datos")

    def close_dialog(self, button):
        """[summary]
        close and delete the add trip dialog
        """
        self.add_request_dialog.dismiss()
        self.add_request_dialog = None
