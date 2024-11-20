from uuid import UUID
from typing import Optional, List
from ninja import Schema


class ErrorSchema(Schema):
    error: str = 'Error'
    message: str
    detail: Optional[str]

class QuerySchema(Schema):
    filters: Optional[dict] = None
    sort: Optional[List[str]] = None

class CoreGenericSchema(Schema):
    id: Optional[UUID] = None
    code: Optional[str] = None