
from pydantic import BaseModel, EmailStr
import datetime

class UserOutput(BaseModel):
    email: EmailStr
    id:str
    created_at: datetime.datetime