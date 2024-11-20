from ninja import ModelSchema, Schema
from typing import List, Optional,Any
from uuid import UUID
from .models import Project, Container, ContainerRelation, Product, ProductDependency, Bundle
from core.schemas import (
                        RelationTypeSchema
                        )
from helpers.schemas import CoreGenericSchema


class ProjectSchema(ModelSchema):
    class Meta:
        model = Project
        fields = '__all__'
        fields_optional = '__all__'

class ContainerInSchema(ModelSchema):
    class Meta:
        model = Container
        fields = '__all__'
        fields_optional = '__all__'

class ContainerSchema(ModelSchema):
    container_type: Optional[CoreGenericSchema] = None
    class Meta:
        model = Container
        fields = '__all__'
        fields_optional = '__all__'

    @staticmethod
    def resolve_container_type(obj):
        return {
            'code':obj.container_type.code,
            'id': obj.container_type.id,
                }

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
    element: Optional[CoreGenericSchema] = None
    data_type: Optional[CoreGenericSchema] = None
    step: Optional[CoreGenericSchema] = None
    status: Optional[CoreGenericSchema] = None
    class Meta:
        model = Product
        fields = "__all__"
        fields_optional = '__all__'

    @staticmethod
    def resolve_element(obj):
        return {
            'code':obj.element.code,
            'id': obj.element.id,
                }
    @staticmethod
    def resolve_data_type(obj):
        return {
            'code':obj.data_type.code,
            'id': obj.data_type.id,
                }
    @staticmethod
    def resolve_step(obj):
        return {
            'code':obj.step.code,
            'id': obj.step.id,
                }
    @staticmethod
    def resolve_status(obj):
        return {
            'code':obj.status.code,
            'id': obj.status.id,
                }

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
    bundle_type: Optional[CoreGenericSchema] = None
    status: Optional[CoreGenericSchema] = None
    step: Optional[CoreGenericSchema] = None
    class Meta:
        model = Bundle
        fields = "__all__"
        fields_optional = '__all__'

    @staticmethod
    def resolve_status(obj):
        return {
            'code':obj.status.code,
            'id': obj.status.id,
                }
    @staticmethod
    def resolve_bundle_type(obj):
        return {
            'code':obj.bundle_type.code,
            'id': obj.bundle_type.id,
                }
    @staticmethod
    def resolve_step(obj):
        return {
            'code':obj.step.code,
            'id': obj.step.id,
                }