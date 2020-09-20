import requests
import json
import uuid


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
            
            # Refresh self.data
            user_data = requests.get(f'https://remasterautostop-fc4ec.firebaseio.com/users/{login_data["localId"]}.json')
            APP.data = json.loads(user_data.content.decode())
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
        APP.local_id = refresh_req.json()['user_id']
        user_data = requests.get(f'https://remasterautostop-fc4ec.firebaseio.com/users/{APP.local_id}.json')
        APP.data = json.loads(user_data.content.decode())
        return True

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