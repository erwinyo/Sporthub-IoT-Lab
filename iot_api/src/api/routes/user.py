# Built-in imports
import os
import sys

# Third-party imports
from loguru import logger
from fastapi import APIRouter, Depends

# Local imports
from base.user import cardcheck, register_user, update_user
from base.config import mysql_conn, mysql_conn_cursor
from api.basemodel.user import MysqlCardCheck, MysqlRegisterUser, MysqlUpdateUser
from utils.response import Response, ApiResponse

logger.remove()
logger.add(sys.stdout, level=os.getenv("LOG_LEVEL"))

router = APIRouter(
    prefix="/user",
    tags=["User"]
)


@router.post("/cardcheck", response_model=ApiResponse)
def cardcheck_api(request: MysqlCardCheck):
    resp_check_card = cardcheck(connection=mysql_conn, connection_cursor=mysql_conn_cursor, card_number=request.card_number)
    if resp_check_card == Response.FORBIDDEN:
        return ApiResponse(status="error", message="Card already registered")
    return ApiResponse(status="success", message="Card is available for register")


@router.post("/register", response_model=ApiResponse)
def register_user_api(request: MysqlRegisterUser):    
    resp_register = register_user(
        connection=mysql_conn, 
        connection_cursor=mysql_conn_cursor,
        data=request
    )
    if resp_register == Response.SUCCESS:
        return ApiResponse(status="success", message="User successfully inserted")
    elif resp_register == Response.SERVER_ERROR:
        return ApiResponse(status="error", message="Failed to register user")

@router.post("/update", response_model=ApiResponse)
def update_user_api(request: MysqlUpdateUser):    
    resp_register = update_user(
        connection=mysql_conn, 
        connection_cursor=mysql_conn_cursor,
        data=request
    )
    if resp_register == Response.SUCCESS:
        return ApiResponse(status="success", message="User successfully updated")
    elif resp_register == Response.SERVER_ERROR:
        return ApiResponse(status="error", message="Failed to update user")