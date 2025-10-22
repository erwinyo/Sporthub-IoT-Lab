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
from nicegui import ui
from nicegui.events import ValueChangeEventArguments

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


uid = None
def submit_data():
    global uid, player_name, dob, email, whatsapp, membership_type

    logger.debug(f"uid: {uid}")
    if uid is None:
        ui.notify("No card has been scanned")
        return
    
    player_name_v = player_name.value
    dob_v = dob.value
    email_v = email.value
    whatsapp_v = whatsapp.value
    membership_type_v = membership_type.value

    logger.debug(f"Player name: {player_name_v}")
    logger.debug(f"DOB: {dob_v}")
    logger.debug(f"Email: {email_v}")
    logger.debug(f"Whatsapp: {whatsapp_v}")
    logger.debug(f"Membership Type: {membership_type_v}")

    if player_name_v == "" or dob_v == "" or email_v == "" or whatsapp_v == "" or membership_type_v == "":
        ui.notify("Please fill all fields")
        return 
    
    
    post_request(
        url=f"http://{os.getenv('IOT_API_HOST')}:{os.getenv('IOT_API_PORT')}/user/register",
        data={
            "id": int(datetime.now().strftime("%Y%m%d%S")),
            "uid": uid,
            "player_name": player_name_v,
            "dob": dob_v,
            "email": email_v,
            "whatsapp": whatsapp_v,
            "membership_type": membership_type_v
        },
        headers={
            'Content-Type': 'application/json'
        }
    )


def verify_id(id_str):
    pattern = re.compile(r'^[A-F0-9]{8}$')
    return bool(pattern.match(id_str))


def register_card():
    global uid, id_card, status_card
    try:
        arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)
        logger.info(f"Connected to: {arduino.name}")
    except Exception as e:
        logger.error(f"Serial connection failed: {e}")
        sys.exit()

    
    while True:
        if arduino.in_waiting > 0:
            captured_data = arduino.readline().decode('utf-8', errors='ignore').strip()
            if captured_data: 
                # Check line is valid or no
                if not verify_id(captured_data):
                    logger.error("The ID is not valid, try different card")
                logger.debug(f"Captured data: {captured_data}")
                id_card.set_text(captured_data)

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
                #     status_card.set_text("Card already registered!")
                #     logger.error(f"Error to register card: {message}")
                #     break
                # else:
                #     uid = captured_data
                #     status_card.set_text("Card Available for Register!")
                #     logger.success(message)
                #     break


                uid = captured_data
                break



ui.markdown('#Sporthub Play')
with ui.row():
    with ui.column():
        ui.button('Register card', on_click=register_card)
    with ui.column():
        with ui.row():
            ui.label("Card ID: ")
            id_card = ui.label()
        with ui.row():
            status_card = ui.label()
player_name = ui.input(label='Player Name', placeholder='')
with ui.input('Date') as dob:
    with ui.menu().props('no-parent-event') as menu:
        with ui.date().bind_value(dob):
            with ui.row().classes('justify-end'):
                ui.button('Close', on_click=menu.close).props('flat')
    with dob.add_slot('append'):
        ui.icon('edit_calendar').on('click', menu.open).classes('cursor-pointer')
email = ui.input(label='Email', placeholder='')
whatsapp = ui.input(label='Whatsapp', placeholder='')
membership_type = ui.select(['Daily', 'Employee'], value='Daily')
ui.button('Submit', on_click=submit_data)


ui.run(reload=False)