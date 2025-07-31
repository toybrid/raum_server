from typing import List
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.db.models import Q
from django.db import transaction
from ninja import Router
from ninja.pagination import paginate
from .schema import (
    QuerySchema, CreateSchema, UpdateSchema, QueryIDSchema, BundleSchema, BundleQuerySchema, ProductDependencySchema
    )
from ams.models import (
    Project, Container, Product, ContainerType, Element, DataType, BundleType, Bundle, Status, ProductDependency
    )

router = Router()

entity_lookup = {
    "Project": Project,
    "Container": Container,
    "Product": Product,
    "ContainerType": ContainerType,
    "Element": Element,
    "DataType": DataType,
    "BundleType": BundleType,
    "Status": Status
}


@router.post("/create", response={201:dict, 400:dict}, tags=['AMS-CRUD'])
def create(request, payload: CreateSchema):
    entity = entity_lookup.get(payload.entity)
    if not entity:
        return 400, {'STATUS': 'ERROR', 'message': f'Entity {payload.entity} not found'}
    
    instance = entity.objects.create(**payload.fields)
    return 201,{**model_to_dict(instance), 'entity': payload.entity}


@router.post("/search", response={200:List[dict], 201:List[dict], 400:dict}, tags=['AMS-CRUD'])
@paginate
def search(request, payload: QuerySchema):
    entity = entity_lookup.get(payload.entity)

    if not entity:
        return 400, {'STATUS': 'ERROR', 'message': f'Entity {payload.entity} not found'}
    
    payload_dict = payload.dict()
    filter_q = Q()

    if payload_dict.get('filters'):
        filter_q = Q(**payload_dict['filters'])

    if payload_dict.get('sort'):
        sort_value = payload_dict['sort']

    if payload_dict.get('fields'):
        fields = payload_dict['fields']

    data = entity.objects.filter(filter_q).order_by(*sort_value).values(*fields)
    results = [{**item, 'entity': payload.entity} for item in data ]
    return results


@router.patch("/update", response={200:dict, 201:dict, 400:dict}, tags=['AMS-CRUD'])
def update(request, payload: UpdateSchema):
    entity = entity_lookup.get(payload.entity)
    if not entity:
        return 400, {'STATUS': 'ERROR', 'message': f'Entity {payload.entity} not found'}
    
    if not payload.entity_id:
        return 400, {'STATUS': 'ERROR', 'message': 'Entity ID is required for update'}

    instance = get_object_or_404(entity, id=payload.entity_id)
    updated_instance = instance.update_from_dict(payload.fields)
    
    return 201,{**model_to_dict(updated_instance), 'entity': payload.entity}


@router.post("/get-by-id", response={201:dict, 400:dict}, tags=['AMS-CRUD'])
def get_by_id(request, payload: QueryIDSchema):
    entity = entity_lookup.get(payload.entity)
    if not entity:
        return 400, {'STATUS': 'ERROR', 'message': f'Entity {payload.entity} not found'}
    
    if not payload.entity_id:
        return 400, {'STATUS': 'ERROR', 'message': 'Entity ID is required for update'}

    instance = get_object_or_404(entity, id=payload.entity_id)
    return 201, {**model_to_dict(instance), 'entity': payload.entity}


@router.post("/create-bundle", response={201:BundleSchema, 400:dict}, tags=['AMS-CRUD'])
def create_bundle(request, payload: CreateSchema):    
    clean_payload = payload.fields.copy()
    clean_payload.pop('products')
    instance = Bundle.objects.create(**clean_payload)
    instance.products.set(payload.fields['products'])
    return 201,instance

    
@router.post("/search-bundle", response={200:List[BundleSchema], 201:List[dict], 400:dict}, tags=['AMS-CRUD'])
@paginate
def search_bundle(request, payload: BundleQuerySchema):
    
    payload_dict = payload.dict()
    filter_q = Q()

    if payload_dict.get('filters'):
        filter_q = Q(**payload_dict['filters'])

    if payload_dict.get('sort'):
        sort_value = payload_dict['sort']

    if payload_dict.get('fields'):
        fields = payload_dict['fields']

    results = Bundle.objects.filter(filter_q).order_by(*sort_value)
    return results

@router.post("/create-product-dependency", response={201:ProductDependencySchema, 400:dict}, tags=['AMS-CRUD'])
def create_product_dependency(request, payload: CreateSchema):    
    clean_payload = payload.fields.copy()
    clean_payload.pop('inputs')
    instance = ProductDependency.objects.create(**clean_payload)
    instance.inputs.set(payload.fields['inputs'])
    return 201,instance

@router.get("/get-product-dependency/{uid}", response={200:ProductDependencySchema, 400:dict}, tags=['AMS-CRUD'])
def get_product_dependency(request, uid:int):
    instance = ProductDependency.objects.filter(product=uid)[0]
    return 200, instance