from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.app import MDApp
from functools import partial

from classes import ListIcon

Builder.load_string('''
<NavigationScreen>
    name: "navigation_screen"
    NavigationLayout:
        id: nav_layout

        ScreenManager:
            MDScreen:
                MDBoxLayout:
                    orientation: "vertical"

                    MDToolbar:
                        id: tool_bar
                        title: "Viajes Disponibles"
                        elevation: 10
                        left_action_items: [["menu", lambda x: nav_drawer.set_state()]]

                    ScreenManager:
                        id: screen_manager

        MDNavigationDrawer:
            id: nav_drawer

            MDBoxLayout:
                orientation: "vertical"
                padding: "8dp"
                spacing: "8dp"

                Image:
                    size_hint_y: .3
                    source: "resources/logo2.jpeg"

                ScrollView:
                    MDList:
                        id: nav_list

                MDLabel:
                    id: watermark
                    size_hint_y: .08
                    text_size: (None, 10)
                    theme_text_color: "Secondary"
                    text: "Developed by Luciano Olivares"
                    font_style: "Overline"

''')


class NavigationScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        """[summary]
        Import of the screens that the navigation_layout will have and a dictionary
        is created with them as key and the value is a tuple with 
        the identification that will be given to the screen, the title and the icon
        """
        # Lista de las pantallas, (id, Título("text"), icono)
        from trips_available_screen import TripsAvailableScreen
        from passengers_available_screen import PassengersAvailableScreen
        from settings_screen import SettingsScreen

        self.list_screen = {
            TripsAvailableScreen: ("trips_available_screen", "Viajes Disponibles", "car-multiple"),
            PassengersAvailableScreen:("passengers_available_screen", "Pasajeros Disponibles", "seatbelt"),
            SettingsScreen: ("settings_screen", "Configuración", "settings")
        }

        for screen, details in self.list_screen.items():
            identification, text, icon = details
            self.ids.screen_manager.add_widget(screen(name=identification))
            self.ids.nav_list.add_widget(ListIcon(text=text, icon=icon, on_release=partial(self.button_list_actions, text, identification)))

    def button_list_actions(self, title, identification):
        self.ids.tool_bar.title = title
        self.ids.screen_manager.current = identification
        self.ids.nav_drawer.set_state()
