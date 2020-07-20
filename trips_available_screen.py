from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDTimePicker
from kivymd.uix.screen import MDScreen

kv = '''
<AddTripDialog>
    orientation: "vertical"
    spacing: "8dp"
    size_hint_y: None
    height: "220dp"

    MDTextField:
        id: city_from
        hint_text: "Desde"

    MDTextField:
        id: city_to
        hint_text: "Para"
    
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
    MDFloatLayout:
        MDLabel:
            text: "Viajes Disponibles"
            font_style: "H2"
'''


class AddTripDialog(MDBoxLayout):
    def __init__(self, **kw):
        super().__init__()
        self.ids.hour_picker.on_release = kw["hour_picker"]


class TripsAvailableScreen(MDScreen):
    Builder.load_string(kv)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.app = MDApp.get_running_app()
        self.add_trip_dialog = None
        self.content = None
        # Data
        self.city_from = None
        self.city_to = None
        self.hour = None
        self.n_passenger = int

    def on_pre_enter(self, *args):
        # Add button to Toolbar
        self.tool_bar = self.app.root.current_screen.ids.tool_bar
        self.tool_bar.right_action_items = [["plus", lambda x: self.show_add_trip_dialog()]]

    def show_add_trip_dialog(self):
        if not self.add_trip_dialog:
            self.add_trip_dialog = MDDialog(
                size_hint=(.8, .6),
                title="Añadir Viaje:",
                type="custom",
                content_cls=AddTripDialog(hour_picker=self.show_time_picker),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        text_color=self.app.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="AÑADIR",
                        text_color=self.app.theme_cls.primary_color,
                        on_release=self.add_trip
                    )
                ]
            )
        self.content = self.add_trip_dialog.ids.spacer_top_box.children[0]
        self.add_trip_dialog.open()

    def show_time_picker(self):
        """Open time picker dialog."""
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self, instance, time):
        self.content.ids.hour_label.color = self.app.theme_cls.primary_color
        self.content.ids.hour_label.text = time.strftime("%H:%M")

    def add_trip(self, button):
        self.city_from = self.content.ids.city_from.text
        self.city_to = self.content.ids.city_to.text
        self.hour = self.content.ids.hour_label.text
        self.seats_available = self.content.ids.seats_available.text
        self.add_trip_dialog.dismiss()
        print(f"Add Data To DataBase, {self.city_from} to {self.city_to}, {self.hour}, {self.seats_available} asientos")
        self.add_trip_dialog = None
        
    def close_dialog(self, button):
        self.add_trip_dialog.dismiss()
        self.add_trip_dialog = None 
