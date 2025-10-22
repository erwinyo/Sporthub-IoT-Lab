# Built-in imports
from datetime import date

# Third-party imports
from pydantic import BaseModel

# Local imports


class MysqlCardCheck(BaseModel):
    card_number: str

class MysqlRegisterUser(BaseModel):
    id: int
    uid: str
    player_name: str
    dob: date
    email: str
    whatsapp: int
    membership_type: str