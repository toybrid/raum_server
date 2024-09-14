from ninja import ModelSchema, Schema
from typing import List, Optional, ClassVar
from uuid import UUID
from datetime import datetime
from .models import Project, Container, ContainerRelation, Product, ProductDependency, Bundle
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

class ProductDependencySchema(ModelSchema):
    product: ProductSchema
    dependencies: List[ProductSchema]
    class Meta:
        model = ProductDependency
        fields = "__all__"
        fields_optional = '__all__'
        # model_fields = ['product', 'dependencies']


class ProductDependencySchemaIn(Schema):
    product: Optional[UUID]
    dependencies: List[str]

class BundleSchema(ModelSchema):
    class Meta:
        model = Bundle
        fields = "__all__"
        fields_optional = '__all__'

class BundleSchemaOut(ModelSchema):
    products: List[ProductSchema]
    class Meta:
        model = Bundle
        fields = "__all__"
        fields_optional = '__all__'