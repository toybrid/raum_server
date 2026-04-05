from django.utils import timezone
from typing import List
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from django.db.models import Q
from ninja import Router
from ninja.pagination import paginate
from .schema import (
    QuerySchema, CreateSchema, UpdateSchema, QueryIDSchema, BundleSchema, BundleQuerySchema, ProductDependencySchema,
    ApproveProductsSchema, ContainerRelationSchemaOut, ContainerRelationSchema, ContainerRelationUpdateSchema
    )
from ams.models import (
    Project, Container, Product, ContainerType, Element, DataType, BundleType, Bundle, Status, ProductDependency, ContainerRelation, RelationType
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
    "Status": Status,
    "RelationType": RelationType
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


@router.patch("/set-status", response={200:dict, 201:dict, 400:dict}, tags=['AMS-CRUD'])
def set_status(request, payload: ApproveProductsSchema):
    status = get_object_or_404(Status, code=payload.status)
    products = Product.objects.filter(id__in=payload.product_ids)

    for product in products:
        product.status = status
        if status.code == 'approved':
            product.approved_at =  timezone.now()
            product.approved_by = payload.username
    
    # Bulk update to optimize database writes, this will not trigger django save() method or signals
    # This is a direct change into database do not take care of any django specific logic
    # Product.objects.bulk_update(products, ['status', 'approved_by'])
    Product.objects.bulk_update(products, ['status', 'approved_at', 'approved_by'])

    return 201, {'STATUS': 'SUCCESS', 'message': f'Approved {products.count()} products.'}


@router.post("/container-relation", response={201: ContainerRelationSchemaOut}, tags=['AMS-CRUD'])
def create_container_realtion(request, payload: ContainerRelationSchema):
    """
    Creates a new relationship between containers.

    Parameters:
    request (Request): The incoming request object.
    payload (ContainerRelationSchema): The relationship data to be created. This includes the IDs of the from_container,
                                      to_containers, and relation_type.

    Returns:
    tuple: A tuple containing the HTTP status code and the created relationship object.
           If an error occurs during the creation process, a 400 status code and an error message are returned.
           If the relationship already exists, a 400 status code and an error message are returned.
    """
    from_container = get_object_or_404(Container, id=payload.from_container)
    to_containers = Container.objects.filter(id__in=payload.to_containers)
    relation_type = get_object_or_404(RelationType, id=payload.relation_type)

    if ContainerRelation.objects.filter(
        from_container=from_container,
        relation_type=relation_type
    ).exists():
        return 400, {'message': str("Relationship already exists")}
    
    relationship_obj = ContainerRelation.objects.create(
        from_container=from_container,
        relation_type=relation_type
    )
    relationship_obj.to_containers.set(to_containers)
    relationship_obj.created_by = payload.created_by
    relationship_obj.modified_by = payload.updated_by
    relationship_obj.save()
    return 201, relationship_obj


@router.patch("/container-relation/{uid}", response={200: ContainerRelationSchemaOut}, tags=['AMS-CRUD'])
def update_container_realtion(request, uid, payload: ContainerRelationUpdateSchema):
    """
    Updates an existing relationship between containers.

    Parameters:
    request (Request): The incoming request object.
    uid (str): The unique identifier of the relationship to be updated.
    payload (ContainerRelationSchema): The updated relationship data. This includes the IDs of the to_containers.

    Returns:
    ContainerRelation: The updated relationship object.
    """
    relationship_obj = get_object_or_404(ContainerRelation, id=uid)
    to_containers = Container.objects.filter(id__in=payload.to_containers)
    relationship_obj.to_containers.set(to_containers)
    relationship_obj.modified_by = payload.updated_by
    relationship_obj.save()
    return relationship_obj


@router.get("/container-relation/{cid}/{rid}", response={200: List[ContainerRelationSchemaOut]}, tags=['AMS-CRUD'])
def get_container_relations(request, cid, rid):
    """
    Retrieves a list of relationships between containers based on the provided from_container and relation_type.

    Parameters:
    request (Request): The incoming request object.\n
    cid (str): The unique identifier of the from_container.\n
    rid (str): The unique identifier of the relation_type.

    Returns:
    List[ContainerRelationSchema]: A list of relationship objects that match the provided from_container and relation_type.
    """
    relationship_obj = ContainerRelation.objects.filter(
                                                from_container=cid, 
                                                relation_type=rid
                                                )
    return relationship_obj