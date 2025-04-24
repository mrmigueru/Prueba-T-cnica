import requests
import base64
import json
from datetime import datetime

class PruebaAPI:
    def __init__(self, email):
        self.email = email
        self.key = None
        self.secret = None
        self.auth_token = None
        self.temporal_auth_token = None
        self.username = None
        
    def register_email(self):
        url = "https://ondemand.fonet.com.ve/cpanel/API_v1/demo/register"
        headers = {
            "accept": "application/json"
        }
        data = {
            "email": self.email
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            self.key = result.get('key')
            self.secret = result.get('secret')
            print("Registro exitoso:")
            print(f"Key: {self.key}")
            print(f"Secret: {self.secret}")
            return True
        else:
            print(f"Error en el registro: {response.status_code} - {response.text}")
            return False
    
    def generate_auth_token(self):
        if not self.key or not self.secret:
            print("No se tiene key o secret. Primero debe registrar el email.")
            return False
            
        auth_string = f"{self.key}:{self.secret}"
        self.auth_token = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        print(f"Token de autenticación generado: {self.auth_token}")
        return True
    
    def get_temporal_token(self):
        if not self.auth_token:
            print("No se tiene auth token. Primero debe generarlo.")
            return False
            
        url = "https://ondemand.fonet.com.ve/cpanel/API_v1/demo/get_token"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            self.temporal_auth_token = result.get('temporal_auth_token')
            self.username = result.get('username')
            print("Token temporal obtenido:")
            print(f"Token: {self.temporal_auth_token}")
            print(f"Expira en: {result.get('expiration')} segundos")
            return True
        else:
            print(f"Error al obtener token temporal: {response.status_code} - {response.text}")
            return False
    
    def send_challenge_data(self, phone, tester_name, project_url):

        if not self.temporal_auth_token:
            print("No se tiene token temporal. Primero debe obtenerlo.")
            return False
            
        url = "https://ondemand.fonet.com.ve/cpanel/API_v1/demo/challenge_me"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.temporal_auth_token}"
        }
        data = {
            "phone": phone,
            "tester_name": tester_name,
            "project_url": project_url
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("Datos enviados exitosamente:")
            print(json.dumps(result, indent=2))
            return True
        else:
            print(f"Error al enviar datos: {response.status_code} - {response.text}")
            return False


if __name__ == "__main__":

    email = "miguelarcila2002@mail.com"  # email
    phone = "+584244948137"          # teléfono
    tester_name = "miguel vargas"       # nombre
    project_url = "https://github.com/mrmigueru/Prueba-T-cnica"  # GitHub
    

    fonet_demo = PruebaAPI(email)
    

    if fonet_demo.register_email():

        if fonet_demo.generate_auth_token():

            if fonet_demo.get_temporal_token():

                fonet_demo.send_challenge_data(phone, tester_name, project_url)