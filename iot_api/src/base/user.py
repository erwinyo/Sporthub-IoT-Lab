# Built-in import
import re
import os
import sys
import time

# Third-party import
import pymysql
from loguru import logger

# Local import
from utils.response import Response


def cardcheck(connection, connection_cursor, card_number):
    # Check user already registered or not
    sql = f"SELECT * FROM `user` WHERE `UID` = '{card_number}';"
    connection_cursor.execute(sql)
    retrieved_ids = connection_cursor.fetchall()
    if len(retrieved_ids) > 0:
        logger.error("User already registered with this card!")
        return Response.FORBIDDEN
    return Response.SUCCESS


def register_user(connection, connection_cursor, data):
    """"
        Registering user
        Args:
            connection: database connection
            connection_cursor: database cursor connection
            data: user data
            {
                "id": str,
                "uid": str,
                "player_name": str,
                "dob": str,
                "email": str,
                "whatsapp": str,
                "membership_type: str
            }
    """
    logger.info("Register user request received")
    logger.debug(f"Data: {data}")

    # ABANDONED : because the card can re-register again
    # Card check
    # try:
    #     response = cardcheck(connection=connection, connection_cursor=connection_cursor, card_number=data.uid)
    #     if response == Response.FORBIDDEN:
    #         return Response.FORBIDDEN
    # except Exception as e:
    #     logger.error(f"Failed to cardcheck: {e}")
    #     return Response.SERVER_ERROR
    
    # Insert to database
    try:
        connection_cursor.connection.ping()
        sql = f"INSERT INTO `user` (`ID`, `UID`, `PlayerName`, `DoB`, `Email`, `WhatsApp`, `MembershipType`) VALUES ('{data.id}', '{data.uid}', '{data.player_name}', '{data.dob}', '{data.email}', '{data.whatsapp}', '{data.membership_type}')"
        connection_cursor.execute(sql)
        connection_cursor.connection.commit()
        logger.success("Successfully inserted a data to database")
        return Response.SUCCESS
    except Exception as e:
        logger.error(f"Failed to insert data to database: {e}")
        return Response.SERVER_ERROR



def update_user(connection, connection_cursor, data):
    """"
        Updating user
        Args:
            connection: database connection
            connection_cursor: database cursor connection
            data: user data
            {
                "id": str,
                "uid": str,
                "player_name": str,
                "dob": str,
                "email": str,
                "whatsapp": str,
                "membership_type: str
            }
    """
    logger.info("Update user request received")
    logger.debug(f"Data: {data}")
    
    # Insert to database
    try:
        connection_cursor.connection.ping()
        sql = f"UPDATE `user` SET `UID` = '{data.uid}', `PlayerName` = '{data.player_name}', `DoB` = '{data.dob}', `Email` = '{data.email}', `WhatsApp` = '{data.whatsapp}', `MembershipType` = '{data.membership_type}' WHERE `ID` = '{data.id}' "
        connection_cursor.execute(sql)
        connection_cursor.connection.commit()
        logger.success("Successfully inserted a data to database")
        return Response.SUCCESS
    except Exception as e:
        logger.error(f"Failed to insert data to database: {e}")
        return Response.SERVER_ERROR

