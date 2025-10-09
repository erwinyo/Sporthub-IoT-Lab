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

    # Check user already registered or not
    sql = f"SELECT * FROM `user` WHERE `ID` = '{data.id}';"
    connection_cursor.execute(sql)
    retrieved_ids = connection_cursor.fetchall()
    if len(retrieved_ids) > 0:
        logger.error("User already registered with this card!")
        return Response.FORBIDDEN

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

