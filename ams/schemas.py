from ninja import ModelSchema, Schema
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from .models import Project, Container, ContainerRelation, Product, ProductDependency
from core.schemas import RelationTypeSchema
from account.schemas import UserSchemaOut

class ProjectSchema(ModelSchema):
    class Meta:
        model = Project
        fields = '__all__'
        fields_optional = '__all__'

class ContainerSchema(ModelSchema):
    class Meta:
        model = Container
        fields = '__all__'
        fields_optional = '__all__'

class ContainerRelationSchema(ModelSchema):
    class Meta:
        model = ContainerRelation
        fields = "__all__"
        fields_optional = '__all__'

class ContainerRelationSchemaOut(ModelSchema):
    from_container: ContainerSchema
    relation_type: RelationTypeSchema
    to_containers: List[ContainerSchema]
    class Meta:
        model = ContainerRelation
        fields = "__all__"
        fields_optional = '__all__'

class ProductSchema(ModelSchema):
    class Meta:
        model = Product
        fields = "__all__"
        fields_optional = '__all__'

class ProductDenendencySchema(ModelSchema):
    # product = ProductSchema
    # dependencies = List[ProductSchema]
    class Meta:
        model = ProductDependency
        fields = "__all__"
        fields_optional = '__all__'

class ProductDenendencySchemaIn(Schema):
    product: Optional[UUID]
    dependencies: List[str]