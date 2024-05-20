from typing import Optional
from pydantic import BaseModel


class DataToken(BaseModel):
    id: Optional[str] = None