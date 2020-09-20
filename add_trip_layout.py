from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.uix.picker import MDTimePicker, MDDatePicker
from kivymd.app import MDApp

Builder.load_string('''
<AddTripLayout>
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
            on_release: root.show_date_picker()

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
            on_release: root.show_time_picker()
    
    MDTextField:
        id: seats
''')

APP = MDApp.get_running_app()

class AddTripLayout(MDBoxLayout):
    def __init__(self, **kw):
        super().__init__()
        self.ids.seats.hint_text = kw["seats"]


    def show_date_picker(self):
        date_dialog = MDDatePicker(callback=self.get_date)
        date_dialog.open()
    
    def get_date(self, date):
        self.ids.date_label.color = APP.theme_cls.primary_color
        self.ids.date_label.text = date.strftime("%d/%m/%Y")

    def show_time_picker(self):
        """Open time picker dialog."""
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.get_time)
        time_dialog.open()

    def get_time(self, instance, time):
        self.ids.hour_label.color = APP.theme_cls.primary_color
        self.ids.hour_label.text = time.strftime("%H:%M")