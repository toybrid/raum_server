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

class ContainerInSchema(ModelSchema):
    class Meta:
        model = Container
        fields = '__all__'
        fields_optional = '__all__'

class ContainerSchema(ModelSchema):
    container_type: dict
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
    @staticmethod
    def resolve_project(obj):
        return {
            'code':obj.project.code,
            'id': obj.project.id,
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
    element: dict
    data_type: dict
    step: dict
    status: dict
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
    # bundle_type: dict
    # status: dict
    # step: dict
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

class QuerySchema(Schema):
    filters: Optional[dict] = {}
    sort: Optional[List[str]] = None