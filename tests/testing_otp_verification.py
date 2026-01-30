import requests
import json

BASE_URL = "http://localhost:8000/api"

def _get_json_sting(data:dict) -> str:
    return json.dumps(data)

def test_user_registration():
    url = BASE_URL + "/user/register"
    post_data:dict = {
        "firstName": "John",
        "lastName": "Doe",
        "email": "rksinghdimapur@gmail.com",
        "password": "SecurePass123!",
    }
    
    response = requests.post(url=url, data=_get_json_sting(post_data), headers={"Content-Type": "application/json"})

    print("Status Code:", response.status_code)
    print("Response Body:", response.json())

    if response.status_code == 201:
        return response.json()


def verify_otp(user:dict):
    url = "http://localhost:8000/api/user/verify"
    post_data:dict = {
        "email": user.get("email"),
        "otp": user.get("otp"),
    }

    json_data = _get_json_sting(post_data)
    
    response = requests.post(url=url, data=json_data, headers={"Content-Type": "application/json"})

    print("Status Code:", response.status_code)
    print("Response Body:", response.json())

    if response.status_code == 200:
        return response.json()

if __name__ == "__main__":
    # registration_response = test_user_registration()
    user = {
        "email": "rksinghdimapur@gmail.com",
        "otp": "043235"  # Replace with the actual OTP received
    }

    verify_otp(user)
    