import requests
import base64
import json
from datetime import datetime, timedelta

def register_email(email):

    url = "https://ondemand.fonet.com.ve/cpanel/API_v1/demo/register"
    headers = {"accept": "application/json"}
    data = {"email": email}
    

    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return {
            "success": True,
            "data": response.json()
    }


def generate_auth_token(key, secret):

  
    auth_string = f"{key}:{secret}"
    

    auth_bytes = auth_string.encode('utf-8')
    

    auth_token = base64.b64encode(auth_bytes).decode('utf-8')
    
    return auth_token


def get_temporal_token(auth_token):

    url = "https://ondemand.fonet.com.ve/cpanel/API_v1/demo/get_token"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return {
            "success": True,
            "data": response.json()
        }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }
    except json.JSONDecodeError:
        return {
            "success": False,
            "error": "La respuesta no tiene formato JSON válido"
        }
    
def send_personal_info(temp_token, phone, name, repo_url):
    url = "https://ondemand.fonet.com.ve/cpanel/API_v1/demo/challenge_me"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {temp_token}"
    }
    data = {
        "phone": phone,
        "tester_name": name,
        "project_url": repo_url
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}
    except json.JSONDecodeError:
        return {"success": False, "error": "La respuesta no tiene formato JSON válido"}


def format_expiration(seconds):

    expiration_time = datetime.now() + timedelta(seconds=seconds)
    return expiration_time.strftime("%Y-%m-%d %H:%M:%S")


def main():
    
    # Registro
    user_email = input("Por favor, ingrese su correo electrónico: ")
    registration_result = register_email(user_email)
    
    if not registration_result["success"]:
        print("\n Error en el registro:")
        print(registration_result["error"])
        return
    
    print("\n Registro exitoso!")
    response_data = registration_result["data"]
    print("Datos de registro recibidos:")
    print(json.dumps(response_data, indent=2))
    
    key = response_data.get("key")
    secret = response_data.get("secret")
    
    if not key or not secret:
        print("\n Error: La respuesta no contiene key o secret")
        return
    
    # token de autenticación

    auth_token = generate_auth_token(key, secret)
    print(" Token de autenticación generado:")
    print(auth_token)
    
    # token temporal
    temporal_token_result = get_temporal_token(auth_token)
    
    if not temporal_token_result["success"]:
        print(" Error al obtener token temporal:")
        print(temporal_token_result["error"])
        return
    
    temporal_data = temporal_token_result["data"]
    print("\n Token temporal obtenido exitosamente!")
    print(" Detalles del token temporal:")
    print(f"  - Token: {temporal_data['temporal_auth_token']}")
    print(f"  - Usuario: {temporal_data['username']}")
    print(f"  - Expira en (segundos): {temporal_data['expiration']}")
    print(f"  - Fecha estimada de expiración: {format_expiration(temporal_data['expiration'])}")
    
    # información personal
    print("Por favor complete la siguiente información:")
    
    phone = input(" Teléfono de contacto: ")
    name = input(" Nombre completo: ")
    repo_url = input("🔗 URL del repositorio GitHub: ")
    
    print("\n⏳ Enviando información...")
    personal_info_result = send_personal_info(
        temporal_data['temporal_auth_token'],
        phone,
        name,
        repo_url
    )
    
    if not personal_info_result["success"]:
        print(" Error al enviar información personal:")
        print(personal_info_result["error"])
        
        # Verificar si el error fue por token expirado
        if "401" in personal_info_result["error"]:
            print("\n El token temporal podría haber expirado.")
            print("Por favor ejecute el programa nuevamente para generar un nuevo token.")
        return
    
    final_data = personal_info_result["data"]
    print(" Resultados finales:")
    print(f"  - Usuario: {final_data['username']}")
    print(f"  - Fecha de registro: {final_data['register_date']}")
    print(f"  - Fecha de completación: {final_data['completion_date']}")
    print("  - Estadísticas:")
    print(f"     * Tiempo generación token temporal: {final_data['statistics']['generate_temp_token_time']}")
    print(f"     * Tiempo total de completación: {final_data['statistics']['total_completion_time']}")

if __name__ == "__main__":
    main()