import time
import hmac
import hashlib
import requests
import uuid
from packages.modules.common import req

# Open API Keys 
ACCESS_KEY = "2xabfbEW4mHagXLnDemxaPllcm6pnX5i"
SECRET_KEY = "Y7jjofZYn4gKgLcDC91surWiZLIAyTpF"
BASE_URL = "https://api-e.ecoflow.com"

def generate_sign(access_key, secret_key, timestamp, nonce):
    message = f"accessKey={access_key}&nonce={nonce}&timestamp={timestamp}"
    
    sign = hmac.new(
        secret_key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()
    
    return sign

def get_devices():
    timestamp = str(int(time.time() * 1000))
    nonce = str(uuid.uuid4())

    sign = generate_sign(ACCESS_KEY, SECRET_KEY, timestamp, nonce)

    headers = {
        "accessKey": ACCESS_KEY,
        "timestamp": timestamp,
        "nonce": nonce,
        "sign": sign,
        "Content-Type": "application/json"
    }

    # url = f"{BASE_URL}/iot-open/sign/device/list"
    #url = f"{BASE_URL}/iot-open/sign/device/system/main/sn?sn=BK31ZE1A4H4J1645"
    url = f"{BASE_URL}/iot-open/sign/device/quota/all?sn=BK31ZE1A4H4J0163"
    # response = requests.get(url, headers=headers)
    response = req.get_http_session().get(
        url,
        headers=headers,
        timeout=10
    ).json()

    # print("Status:", response.status_code)
    # print("Response:", response.text)
    print(response)

get_devices()