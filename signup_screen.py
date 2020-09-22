from functools import partial

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from myfirebase import Signup

Builder.load_string('''
<SignupScreen>:
    name: "signup_screen"

    # Header (BackScreenButton / Title)
    MDFloatingActionButton:
        id: back_button
        icon: "arrow-left"
        md_bg_color: app.theme_cls.primary_color
        pos_hint: {"center_x": .15, "center_y": .9}
    
    MDLabel:
        text: "Registro"
        halign: "center"
        font_style: "H3"
        pos_hint: {"center_x": .5, "center_y": .9}

    # TextInputs Passenger
    MDTextFieldCustom:
        id: name
        hint_text: "Nombre"
        pos_hint: {"center_x": .5, "center_y": .8}
        size_hint_x: .8
        focus: True
        on_text_validate: last_name.focus = True
    
    MDTextFieldCustom:
        id: last_name
        hint_text: "Apellido"
        pos_hint: {"center_x": .5, "center_y": .75}
        size_hint_x: .8
        on_text_validate: email.focus = True
    
    MDTextFieldCustom:
        id: email
        hint_text: "Correo Electrónico"
        pos_hint: {"center_x": .5, "center_y": .7}
        size_hint_x: .8
        on_text_validate: password.focus = True
    
    MDTextFieldCustom:
        id: password
        hint_text: "Contraseña"
        password: True
        pos_hint: {"center_x": .5, "center_y": .65}
        size_hint_x: .8
        on_text_validate: confirm_password.focus = True

    MDTextFieldCustom:
        id: confirm_password
        hint_text: "Confirmar Contraseña"
        password: True
        pos_hint: {"center_x": .5, "center_y": .6}
        size_hint_x: .8
        on_text_validate: cel_number.focus = True
    
    MDTextFieldCustom:
        id: cel_number
        hint_text: "Número de Celular (+569XXXXXXXX)"
        pos_hint: {"center_x": .5, "center_y": .55}
        size_hint_x: .8

    # CheckBox Driver
    MDLabel:
        text: "Conductor"
        pos_hint: {"center_x": .4, "center_y": .5}
        size_hint_x: .5
    
    MDCheckbox:
        id: driver_check
        group: 'test'
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint: (.07, .05)

    # TextInputs Driver Data
    MDTextFieldCustom:
        id: rut
        hint_text: "Rut (11.111.111-K)"
        disabled: not driver_check.active
        pos_hint: {"center_x": .5, "center_y": .45}
        size_hint_x: .8

    MDTextFieldCustom:
        id: plate
        hint_text: "Patente (XX-XX-XX)"
        disabled: not driver_check.active
        pos_hint: {"center_x": .5, "center_y": .4}
        size_hint_x: .8

    MDLabel:
        id: error_label
        pos_hint: {"center_x": .5, "center_y": .31}
        size_hint_x: .3
        theme_text_color: "Error"
        halign: "center"

    MDRaisedButton:
        id: signup_button
        pos_hint: {"center_x": .5, "center_y": .25}
        size_hint_y: .06
        text: "Registrar"
        font_size: 30
''')

APP = MDApp.get_running_app()
SIGNUP = Signup()

class SignupScreen(MDScreen):
    def on_pre_enter(self):
        """[summary]
        When entering the screen it initializes the functions
        to their respective buttons within it
        """
        self.ids.back_button.bind(on_release=self.change_screen)
        self.ids.signup_button.bind(on_release=self.signup_button_action)

    def signup_button_action(self, instance):
        """[summary]
        Check if the driver checkbox is activated if it is not, 
        yhe user registers with two less parameters (rut and plate)
        """
        name = self.ids.name.text
        last_name = self.ids.last_name.text
        email = self.ids.email.text
        password = self.ids.password.text
        confirm_password = self.ids.confirm_password.text
        cel_number = self.ids.cel_number.text
        rut = self.ids.rut.text
        plate = self.ids.plate.text
        error_label = self.ids.error_label
        if name != "" and last_name != "" and email != "" and password != "" and cel_number != "":
            if password == confirm_password:
                if 12 > len(password) > 6 :
                    if cel_number[0] == "+" and len(cel_number) == 12:
                        if self.ids.driver_check.active:
                            if len(plate) == 8:
                                if 13 > len(rut) >= 11:
                                    self.create_user(name, last_name, email, password, cel_number, rut, plate, True)
                                else:
                                    error_label.text = "Rut Incorrecto"
                            else:
                                error_label.text = "Patente Incorrecta"
                        else:
                            #En caso de que sea solo pasajero
                            self.create_user(name, last_name, email, password, cel_number)
                    else:
                        error_label.text = "Número de Celular Invalido"
                else:
                    error_label.text = "La Contraseña Debe Contener\nEntre 6 y 12 Caracteres"
            else:
                error_label.text = "Las Contraseñas No Coinciden\nFavor Verificar"
        else:
            error_label.text = "Debes Completar todos los campos"

    def create_user(self, name, last_name, email, password, cel_number, rut=None, plate=None, driver=False):
        if driver:
            SIGNUP.signup(
                            name = name,
                            last_name = last_name,
                            email = email,
                            password = password,
                            cel_number = cel_number,
                            rut = rut,
                            plate = plate,
                            driver=driver
                    )
        else:
            SIGNUP.signup(
                        name = name,
                        last_name = last_name,
                        email = email,
                        password = password,
                        cel_number = cel_number,
                    )

    def change_screen(self, instance):
        APP.root.current= "login_screen"