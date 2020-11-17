import requests
import json
import uuid
from kivymd.app import MDApp
from kivy.network.urlrequest import UrlRequest
from navigation_screen import NavigationScreen

APP = MDApp.get_running_app()

def exchange_refresh_token():
    with open("resources/refresh_token.txt", 'r') as f:
        refresh_token = f.read()
        
    refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + APP.WAK
    refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
    refresh_req = requests.post(refresh_url, data=refresh_payload)

    localId = refresh_req.json()['user_id']
    refresh_data(localId)

def refresh_data(localId):
    # Pasar requests a UrlResquest 
    APP.localId = localId
    data_url = f'https://remasterautostop-fc4ec.firebaseio.com/users/{APP.localId}.json'
    user_data = UrlRequest(data_url, on_success=load_navigation_screen)

def load_navigation_screen(request, result):
    # SAVE USER DATA ON THE APP AND LOAD THE NAVIGATION_SCREEN
    APP.data = result

    if not APP.root.has_screen("navigation_screen"):
        APP.root.add_widget(NavigationScreen())
    APP.root.remove_widget(APP.root.get_screen("startup_screen"))
    APP.root.current = "navigation_screen"



class Signup():
    @staticmethod
    def signup_passenger(localId, new_user_data):
        post_request = requests.patch(
            f'https://remasterautostop-fc4ec.firebaseio.com/users/{localId}.json',
            data=json.dumps(new_user_data)
        )
        if not post_request.ok:
            return False
        return True

    @staticmethod
    def signup_driver(localId, driver_data):
        post_request = requests.patch(
            f'https://remasterautostop-fc4ec.firebaseio.com/users/{localId}/driver.json',
            data=json.dumps(driver_data)
        )
        if not post_request.ok:
            return False
        return True

    def signup(self, email, password, name, last_name, cel_number, rut=None, plate=None, driver=False):
        signup_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key=" + APP.WAK
        signup_payload = {
            "email": email,
            "password": password}
        signup_request = requests.post(signup_url, data=signup_payload)
        signup_data = json.loads(signup_request.content.decode())

        if signup_request.ok:
            new_user_data = {
                    'name': name,
                    'last_name': last_name,
                    'cel_number': cel_number,
                    'driver': {}
                }
            was_registered = self.signup_passenger(signup_data["localId"], new_user_data)

            if was_registered:
                if driver:
                    driver_data = {
                            'rut': rut,
                            'plate': plate
                        }
                    was_registered = self.signup_driver(signup_data["localId"], driver_data)

                    if was_registered:
                        APP.root.current = "login_screen"  
                        print("REGISTRO COMPLETO DE CONDUCTOR")
                    else:
                        self.delete_account(email, password)
                        print("ERROR AL REGISTRAR LOS DATOS DE CONDUCTOR")
                else:
                    APP.root.current = "login_screen"  
                    print("REGISTRO COMPLETO DE PASAJERO")
            else:
                self.delete_account(email, password)
                print("ERROR AL REGISTRAR LOS DATOS DE PASAJERO")
        else:
            print(signup_data["error"]["message"])

    def delete_account(self, email, password):
        login_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + APP.WAK
        login_payload = {"email": email, "password": password, "returnSecureToken":True}
        login_request = requests.post(login_url, data=login_payload)
        login_data = json.loads(login_request.content.decode())

        delete_account_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/deleteAccount?key=" + APP.WAK
        delete_payload = {
            "idToken": login_data["idToken"],
            "localId": login_data["localId"]
        }
        signout_request = requests.post(delete_account_url, data=delete_payload)
        return signout_request
    
class Database():

    @staticmethod
    def create_new_trip(name, last_name, city_from, city_to, date, hour, seats_available, cel_number, plate):
        n_trip = uuid.uuid1()
        trip_data = {
            "driver": f'{name} {last_name}',
            "city_from": city_from,
            "city_to": city_to,
            "date": date,
            "hour": hour,
            "seats_available": seats_available,
            "cel_number": cel_number,
            "plate": plate
        }

        patch_request = requests.patch(
            f'https://remasterautostop-fc4ec.firebaseio.com/trips_available/{n_trip}.json',
            data=json.dumps(trip_data)
        )

    @staticmethod
    def update_trip(trip_id, city_from, city_to, date, hour, seats_available):
        trip_data = {
            "city_from": city_from,
            "city_to": city_to,
            "date": date,
            "hour": hour,
            "seats_available": seats_available
        }

        patch_request = requests.patch(
            f'https://remasterautostop-fc4ec.firebaseio.com/trips_available/{trip_id}.json',
            data=json.dumps(trip_data)
        )
    
    @staticmethod
    def complete_trip(trip_id, driver, city_from, city_to, date, hour, seats_available, cel_number, plate):
        trip_data = {
            "driver": driver,
            "city_from": city_from,
            "city_to": city_to,
            "date": date,
            "hour": hour,
            "seats_available": seats_available,
            "cel_number": cel_number,
            "plate": plate
        }
        patch_request = requests.patch(
            f'https://remasterautostop-fc4ec.firebaseio.com/trips_completed_beta/{trip_id}.json',
            data=json.dumps(trip_data)
        )

    @staticmethod
    def delete_trip(trip_id):
        post_request = requests.delete(f'https://remasterautostop-fc4ec.firebaseio.com/trips_available/{trip_id}.json')

    @staticmethod
    def add_passenger_request(name, last_name, city_from, city_to, date, hour, n_passengers, cel_number):
        n_request = uuid.uuid1()
        request_data = {
            "passenger": f'{name} {last_name}',
            "city_from": city_from,
            "city_to": city_to,
            "date": date,
            "hour": hour,
            "n_passengers": n_passengers,
            "cel_number": cel_number
        }

        post_request = requests.patch(
            f'https://remasterautostop-fc4ec.firebaseio.com/passengers_request/{n_request}.json',
            data=json.dumps(request_data)
        )

    @staticmethod
    def update_request(n_request, city_from, city_to, date, hour, n_passengers):
        request_data = {
            "city_from": city_from,
            "city_to": city_to,
            "date": date,
            "hour": hour,
            "n_passengers": n_passengers
        }

        post_request = requests.patch(
            f'https://remasterautostop-fc4ec.firebaseio.com/passengers_request/{n_request}.json',
            data=json.dumps(request_data)
        )

    @staticmethod
    def complete_request(n_request, passenger, city_from, city_to, date, hour, n_passengers, cel_number):
        request_data = {
            "passenger": passenger,
            "city_from": city_from,
            "city_to": city_to,
            "date": date,
            "hour": hour,
            "n_passengers": n_passengers,
            "cel_number": cel_number
        }
        post_request = requests.patch(
            f'https://remasterautostop-fc4ec.firebaseio.com/passengers_requests_completed_beta/{n_request}.json',
            data=json.dumps(request_data)
        )

    @staticmethod
    def delete_passenger_request(request_id):
        post_request = requests.delete(f'https://remasterautostop-fc4ec.firebaseio.com/passengers_request/{request_id}.json')

    @staticmethod
    def trips_available(type_request):
        get_request = requests.get(f'https://remasterautostop-fc4ec.firebaseio.com/{type_request}.json')
        trips_data = json.loads(get_request.content.decode())
        return trips_data


#MyFirebase().sign_in("luciano@correo.com", "12341234")