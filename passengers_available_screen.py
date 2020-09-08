from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker, MDTimePicker
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel

from kivy.clock import Clock
from trips_banner import TripsBanner
from myfirebase import Database

Builder.load_string('''
<AddRequestDialog>
    orientation: "vertical"
    spacing: "8dp"
    size_hint_y: None
    height: "300dp"

    MDTextField:
        id: city_from
        hint_text: "Desde"

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
        id: n_passengers
        hint_text: "Número de pasajeros"

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

class AddRequestDialog(MDBoxLayout):
    def __init__(self, **kw):
        super().__init__()
        self.ids.hour_picker.on_release = kw["hour_picker"]
        self.ids.date_picker.on_release = kw['date_picker']

class PassengersAvailableScreen(MDScreen):

    def __init__(self, **kw):
        super().__init__(**kw)
        
        self.add_request_dialog = None
        self.content = None
        # Data
        self.city_from = None
        self.city_to = None
        self.hour = None
        self.n_passenger = int
        # Charge Passengers Data
        self.refresh_available_passengers()

    def on_pre_enter(self, *args):
        self.add_request_button.bind(on_release=self.show_add_request_dialog)

    def refresh_available_passengers(self):
        try:
            passengers_data = DATABASE.trips_available("passengers_request")
            for passenger, data in passengers_data.items():
                self.ids.passengers_grid.add_widget(TripsBanner(
                    city_from=data['city_from'],
                    city_to=data['city_to'],
                    name=data['passenger'],
                    cel_number=data['cel_number'],
                    date=data['date'],
                    hour=data['hour'],
                    seats=data['n_passengers'],
                    trip_id=passenger
                ))
        except Exception as e:
            print(e)
            self.ids.passengers_grid.add_widget(MDLabel(text="No hay Pasajeros Disponibles"))
    

    def refresh_callback(self, *args):
        '''A method that updates the state of your application
        while the spinner remains on the screen.'''

        def refresh_callback(interval):
            self.ids.passengers_grid.clear_widgets()
            self.refresh_available_passengers()
            self.ids.refresh_layout.refresh_done()

        Clock.schedule_once(refresh_callback, 1)


    def show_add_request_dialog(self, instance_button):
        """[summary]
        Función encargada de inicializar una ventana emergente en la cual podemos ingresar una nueva
        solicitud de viaje
        """
        if not self.add_request_dialog:
            self.add_request_dialog = MDDialog(
                size_hint=(.8, .7),
                title="Añadir Solicitud:",
                type="custom",
                content_cls=AddRequestDialog(hour_picker=self.show_time_picker,  date_picker=self.show_date_picker),
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

    def add_request(self, button):
        self.city_from = self.content.ids.city_from.text
        self.city_to = self.content.ids.city_to.text
        self.date = self.content.ids.date_label.text
        self.hour = self.content.ids.hour_label.text
        self.n_passengers = self.content.ids.n_passengers.text

        if (self.city_from and self.city_to and self.n_passengers != "" and
            self.date != "Fecha" and self.hour != "Hora"):
            # If All fields are completed the add the request
            DATABASE.add_passenger_request(
                APP.data['name'], APP.data['last_name'],
                self.city_from, self.city_to, self.date, self.hour,
                self.n_passengers, APP.data['cel_number']
            )
            self.close_dialog("")
        else:
            print("Debes Completar Todos Los Datos")

    def close_dialog(self, button):
        self.add_request_dialog.dismiss()
        self.add_request_dialog = None
