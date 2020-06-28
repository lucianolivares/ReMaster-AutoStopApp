import requests
import json


wak = ""

def sign_in(self, email, password):
    signin_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.wak
    signin_payload = {"email": email, "password": password, "returnSecureToken":True}
    signin_request = requests.post(signin_url, data=signin_payload)
    signin_data = json.loads(signin_request.content.decode())
    if signin_request.ok:
        refresh_token = signin_data["refreshToken"]
        with open("refresh_token.txt", "w") as f:
            f.write(refresh_token)
    else:
        print(signin_data["error"]["message"])

def exchange_refresh_token(self, refresh_token):
    refresh_url = "https://securetoken.googleapis.com/v1/token?key=" + self.wak
    refresh_payload = '{"grant_type": "refresh_token", "refresh_token": "%s"}' % refresh_token
    refresh_req = requests.post(refresh_url, refresh_payload)
    print(refresh_req)

try:
    with open("refresh_token.txt", "r") as f:
        refresh_token = f.read()
        exchange_refresh_token(refresh_token)
except:
    print("error")

#sign_in("luciano@correo.com", "12341234")
