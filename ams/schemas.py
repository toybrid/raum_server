from ninja import ModelSchema, Schema
from typing import List, Optional, Union
from datetime import datetime
from uuid import UUID
from .models import Project, Container, ContainerRelation, Product, ProductDependency, Bundle
from core.schemas import (
                        RelationTypeSchema, ContainerTypeSchema, ElementSchema, 
                        DataTypeSchema, StepSchema, BundleTypeSchema, StatusSchema,
                        )

class ProjectSchema(ModelSchema):
    class Meta:
        model = Project
        fields = '__all__'
        fields_optional = '__all__'

class ProjectMinSchema(ModelSchema):
    class Meta:
        model = Project
        fields = ['id', 'code', 'label', 'client_name']
        fields_optional = '__all__'

class ContainerInSchema(ModelSchema):
    class Meta:
        model = Container
        fields = '__all__'
        fields_optional = '__all__'

class ContainerSchema(ModelSchema):
    project: ProjectMinSchema
    container_type: ContainerTypeSchema
    class Meta:
        model = Container
        fields = '__all__'
        fields_optional = '__all__'

class ContainerMinSchema(ModelSchema):
    class Meta:
        model = Container
        fields = ['id', 'code', 'client_name', 'frame_range']
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
    element: ElementSchema
    data_type: DataTypeSchema
    step: StepSchema
    status: StatusSchema
    class Meta:
        model = Product
        fields = "__all__"
        fields_optional = '__all__'

class ProductInSchema(ModelSchema):
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
    product: Optional["UUID"]
    dependencies: List[str]

class BundleSchema(ModelSchema):
    class Meta:
        model = Bundle
        fields = "__all__"
        fields_optional = '__all__'

class BundleSchemaOut(ModelSchema):
    bundle_type: BundleTypeSchema
    products: List[ProductSchema]
    status: StatusSchema
    class Meta:
        model = Bundle
        fields = "__all__"
        fields_optional = '__all__'

class QuerySchema(Schema):
    filters: Optional[dict] = {}
    sort: Optional[str] = None