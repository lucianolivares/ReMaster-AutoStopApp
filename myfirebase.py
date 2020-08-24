import requests
import json

from kivymd.app import MDApp

WAK = ""
APP = MDApp.get_running_app()


class Login():

    def login(self, email, password):
        login_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + WAK
        login_payload = {"email": email, "password": password, "returnSecureToken":True}
        login_request = requests.post(login_url, data=login_payload)
        login_data = json.loads(login_request.content.decode())
        if login_request.ok:
            refresh_token = login_data["refreshToken"]
            with open("resources/refresh_token.txt", "w") as f:
                f.write(refresh_token)
            # Change to NavigationScreen and remove login_screen
            login_screen = APP.root.current_screen
            from navigation_screen import NavigationScreen
            self.nav_screen = NavigationScreen()
            APP.root.add_widget(self.nav_screen)
            APP.root.current = "navigation_screen"
            APP.root.remove_widget(login_screen)
            return True

        else:
            return login_data["error"]["message"]

    def exchange_refresh_token(self):
        with open("resources/refresh_token.txt", 'r') as f:
            refresh_token = f.read()
            
        refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + WAK
        refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
        refresh_req = requests.post(refresh_url, data=refresh_payload)
        id_token = refresh_req.json()['id_token']


class Signup():
    @staticmethod
    def signup_passenger(localId, name, last_name, cel_number):
        new_user_data = {
            'name': name,
            'last_name': last_name,
            'cel_number': cel_number,
            'driver': {}
        }
        post_request = requests.patch(
            f'https://remasterautostop-fc4ec.firebaseio.com/users/{localId}.json',
            data=json.dumps(new_user_data)
        )

    @staticmethod
    def signup_driver(localId, rut, plate):
        driver_data = {
            'rut': rut,
            'plate': plate
        }
        post_request = requests.patch(
            f'https://remasterautostop-fc4ec.firebaseio.com/users/{localId}/driver.json',
            data=json.dumps(driver_data)
        )

    def signup(self, email, password, name, last_name, cel_number, rut=None, plate=None, driver=False):
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + WAK
        signup_payload = {
            "email": email,
            "password": password}
        signup_request = requests.post(signup_url, data=signup_payload)

        signup_data = json.loads(signup_request.content.decode())

        if signup_request.ok:
            self.signup_passenger(signup_data["localId"], name, last_name, cel_number)
            if driver:
                self.signup_driver(signup_data["localId"], rut, plate)
            Login().login(email, password)

        else:
            print(signup_data["error"]["message"])

#MyFirebase().sign_in("luciano@correo.com", "12341234")