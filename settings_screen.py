from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from myfirebase import Signup, Login

Builder.load_string('''
<AddDriverDataLayout>
    orientation: "vertical"
    spacing: "8dp"
    size_hint_y: None
    height: "100dp"
    
    MDTextField:
        id: plate
        on_text_validate: rut.focus = True
        hint_text: "Patente"

    MDTextField:
        hint_text: "Rut"
        id: rut

<SettingsScreen>:
    id: settings_screen
    MDLabel:
        id: name
        font_style: "H3"
        pos_hint: {"x": .15, "top": .8}
        size_hint: (.8, .1)

    MDLabel:
        id: data
        pos_hint: {"x": .1, "top": .6}
        size_hint: (.8, .3)

    MDRaisedButton:
        id: add_driver_data
        text: "Añadir Datos Conductor"
        pos_hint: {"center_x": .5, "center_y": .3}
        md_bg_color: app.theme_cls.accent_color
        
    MDRaisedButton:
        id: log_out_button
        text: "Cerrar Sesion"
        pos_hint: {"center_x": .5, "center_y": .2}
''')

APP = MDApp.get_running_app()
SIGNUP = Signup()
LOGIN = Login()

class AddDriverDataLayout(MDBoxLayout):
    pass


class SettingsScreen(MDScreen):
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.ids.log_out_button.bind(on_release=self.log_out)
        self.ids.add_driver_data.bind(on_release=self.open_add_info)
        self.refresh_driver_data()

    def on_pre_enter(self, *args):
        APP.root.current_screen.ids.tool_bar.right_action_items = []
    

    def refresh_driver_data(self):
        data = APP.data
        self.ids.name.text = data['name'] + "\n" + data['last_name']
        try:
            self.ids.data.text = f"""
            Celular: {data['cel_number']}\n
            Rut: {data['driver']['rut']}\n
            Patente: {data['driver']['plate']}\n
            """
            self.remove_widget(self.ids.add_driver_data)

        except :
            self.ids.data.text = f"""
            Celular: {data['cel_number']}
            """
    def open_add_info(self, instance):
        self.addDriverDataDialog = MDDialog(
            size_hint=(.6, .4),
            title="Añadir Datos de\nConductor:",
            type="custom",
            content_cls=AddDriverDataLayout(),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    text_color=APP.theme_cls.primary_color,
                    on_release=self.close_dialog
                ),
                MDFlatButton(
                    text="AÑADIR", text_color=APP.theme_cls.primary_color,
                    on_release=self.addDriverData
                )
            ]
        )
        self.content = self.addDriverDataDialog.ids.spacer_top_box.children[0]
        self.addDriverDataDialog.open()

    def addDriverData(self, button):
        plate = self.content.ids.plate.text
        rut = self.content.ids.rut.text

        if len(plate) == 8 and 13 > len(rut) >= 11:
            driver_data = {
                        'rut': rut,
                        'plate': plate 
                    }
            # If All fields are completed
            self.close_dialog("")
            SIGNUP.signup_driver(APP.localId, driver_data)
            LOGIN.exchange_refresh_token()
            self.refresh_driver_data()
        else:
            print("Debes Completar Todos Los Datos")

    def close_dialog(self, button):
        self.addDriverDataDialog.dismiss()
        self.addDriverDataDialog = None 

    def log_out(self, instance):
        with open("resources/refresh_token.txt", "w") as f:
            f.write("")

        if not APP.root.has_screen("login_screen"):
            from login_screen import LoginScreen
            self.login_screen = LoginScreen()
            APP.root.add_widget(self.login_screen)
        APP.root.current = "login_screen"
        
        APP.root.remove_widget(APP.root.get_screen("navigation_screen"))