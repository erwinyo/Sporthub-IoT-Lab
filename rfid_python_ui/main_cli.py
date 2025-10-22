# Built-in import
import re
import os
import sys
import time
import serial
from uuid import uuid4
from datetime import datetime
import serial.tools.list_ports

# Third-party import
import pymysql
import requests
from loguru import logger
from dotenv import load_dotenv


# Local import

load_dotenv()

# Logger configuration
logger.remove()
logger.add(sys.stdout, level="TRACE")


def post_request(url, data, headers=None, timeout=10):
    try:
        response = requests.post(url, json=data, headers=headers, timeout=timeout)
        logger.info(f"POST request to {url} succeeded with status code {response.status_code}")
        return response
    except requests.RequestException as e:
        logger.error(f"POST request to {url} failed: {e}")
        return None

def verify_id(id_str):
    pattern = re.compile(r'^[A-F0-9]{8}$')
    return bool(pattern.match(id_str))

def main():
    # Setup serial connection on arduino
    try:
        arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)
        logger.info(f"Connected to: {arduino.name}")
    except Exception as e:
        logger.error(f"Serial connection failed: {e}")
        return
    
    while True:
        if arduino.in_waiting > 0:
            captured_data = arduino.readline().decode('utf-8', errors='ignore').strip()
            if captured_data: 
                # Check line is valid or no
                if not verify_id(captured_data):
                    logger.error("The ID is not valid, try different card")
                logger.debug(f"Captured data: {captured_data}")

                # ABANDONED : because the card can re-register again
                # check card first
                # logger.info(f"Checking card availability...")
                # response = post_request(
                #     url=f"http://{os.getenv('IOT_API_HOST')}:{os.getenv('IOT_API_PORT')}/user/cardcheck", 
                #     data={
                #         "card_number": captured_data
                #     }, headers= {
                #         'Content-Type': 'application/json'
                #     }
                # ).json()
                # status = response["status"]
                # message = response["message"]
                # if status == "error":
                #     logger.error(f"Error to register card: {message}")
                #     continue
                # else:
                #     logger.success(message)

                id = int(datetime.now().strftime("%Y%m%d%S"))
                uid = captured_data
                player_name = input("Player Name: ")
                dob = input("DOB (YYYY-MM-DD): ")
                email = input("Email: ")
                whatsapp = int(input("Whatsapp: "))
                membership_type = input("Membership Type: ")

                response = post_request(
                    url=f"http://{os.getenv('IOT_API_HOST')}:{os.getenv('IOT_API_PORT')}/user/register", 
                    data={
                        "id": id,
                        "uid": uid,
                        "player_name": player_name,
                        "dob": dob,
                        "email": email,
                        "whatsapp": whatsapp,
                        "membership_type": membership_type
                    }, headers= {
                        'Content-Type': 'application/json'
                    }
                ).json()

                status = response["status"]
                message = response["message"]
                if status == "error":
                    logger.error(f"Error to register card: {message}")
                else:
                    logger.success("Success to register card!")
                     
if __name__ == "__main__":
    main()



    
    