# assets/api/schemas.py

from ninja import Schema, ModelSchema
from typing import Optional, Dict, List, Union
from ams.models import Bundle, Product, ProductDependency

class QuerySchema(Schema):
    entity: str
    filters: Optional[Dict] = None
    fields: Optional[List[str]] = None
    sort: Optional[List[str]] = None

class BundleQuerySchema(Schema):
    filters: Optional[Dict] = None
    sort: Optional[List[str]] = None

class UpdateSchema(Schema):
    entity: str
    entity_id: str
    fields: Dict

class CreateSchema(Schema):
    entity: str
    fields: Dict

class QueryIDSchema(Schema):
    entity: str
    fields: Optional[List[str]] = None

class ProductSchema(ModelSchema):
    entity:str = "Product"
    class Config:
        model = Product
        model_fields = "__all__"

class BundleSchema(ModelSchema):
    entity:str = "Bundle"
    products: List[ProductSchema]
    class Config:
        model = Bundle
        model_fields = "__all__"

class ProductDependencySchema(ModelSchema):
    entity:str = "ProductDependency"
    inputs: List[ProductSchema]
    class Config:
        model = ProductDependency
        model_fields = "__all__"

class ApproveProductsSchema(Schema):
    product_ids: List[int]
    username: str
    status: str