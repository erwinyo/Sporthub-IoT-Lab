# Built-in imports
import os
import sys

# Third-party imports
from loguru import logger
from fastapi import APIRouter, Depends

# Local imports
from base.user import register_user
from base.config import mysql_conn, mysql_conn_cursor
from api.basemodel.user import MysqlRegisterUser
from utils.response import Response

logger.remove()
logger.add(sys.stdout, level=os.getenv("LOG_LEVEL"))

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/register")
def register_user_api(request: MysqlRegisterUser):
    resp = register_user(
        connection=mysql_conn, 
        connection_cursor=mysql_conn_cursor,
        data=request
    )
    if resp == Response.SUCCESS:
        return {"status": "success", "message": "User successfully inserted"}
    elif resp == Response.FORBIDDEN:
        return {"status": "error", "message": "User already exists"}

