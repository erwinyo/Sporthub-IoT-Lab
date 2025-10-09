
# Built-in import
import re
import os
import sys
import time
import serial
import serial.tools.list_ports

# Third-party import
import pymysql
from loguru import logger
from dotenv import load_dotenv

# Local import
from utils.database import get_mysql_connection

# Logger configuration
logger.remove()
logger.add(sys.stdout, level=os.getenv("LOG_LEVEL"))


# MySQL database connection
mysql_conn, mysql_conn_cursor = get_mysql_connection(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    db=os.getenv("MYSQL_DB")
)