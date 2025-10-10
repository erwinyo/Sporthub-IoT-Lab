
# Built-in import
import os
import sys

# Third-party import
import pymysql
from loguru import logger
from dotenv import load_dotenv

# Local import

# Logger configuration
logger.remove()
logger.add(sys.stdout, level=os.getenv("LOG_LEVEL"))

def get_mysql_connection(host, user, password, db):
    try:
        conn = pymysql.connect(
            host = host,
            user = user,
            password = password,
            db = db
        )
        conn_cursor = conn.cursor()
        logger.success(f"Database connection successfully {host}:{user}")
        return conn, conn_cursor
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        return
    
    