from ninja import Schema
from typing import Optional


class ErrorSchema(Schema):
    error: str = 'Error'
    message: str
    detail: Optional[str]