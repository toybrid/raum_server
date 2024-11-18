from typing import List
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q
from ninja import Router
from ninja.pagination import paginate
from ams.models import Project, Container, ContainerRelation, Product, ProductDependency, Bundle
from core.models import ContainerType, RelationType, Step, Element, DataType, Status, BundleType
from ams.schemas import (
                    ProjectSchema, ContainerSchema, QuerySchema, ContainerInSchema, ProductInSchema,
                    ContainerRelationSchema, ProductSchema, ContainerRelationSchemaOut,
                    ProductDependencySchema, ProductDependencySchemaIn, BundleSchema, BundleSchemaOut
                    )
from helpers.utils import build_filters
from account.utils import AuthBearer
from pprint import pprint

router = Router()

# -------------------------------- Project --------------------------------

@router.post("/project", response={201: ProjectSchema}, auth=AuthBearer(), tags=['Project'])
def create_project(request, payload: ProjectSchema):
    """
    Creates a new project.

    Parameters:
    request (Request): The incoming request object.
    payload (ProjectSchema): The project data to be created.

    Returns:
    tuple: A tuple containing the HTTP status code and the created project object.
           If an error occurs during the creation process, a 400 status code and an error message are returned.
    """
    project = Project.objects.create(**payload.dict())
    project.created_by = request.auth
    project.modified_by = request.auth
    project.save()
    return 201, project


@router.patch("/project/{uid}", response={200:ProjectSchema}, auth=AuthBearer(), tags=['Project'])
def update_project(request, uid: str, payload: ProjectSchema):
    """
    Updates an existing project.

    Parameters:
    request (Request): The incoming request object.
    uid (str): The unique identifier of the project to be updated.
    payload (ProjectSchema): The updated project data.

    Returns:
    Project: The updated project object.
    """
    project = get_object_or_404(Project, id=uid)
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(project, attr, value)

    project.modified_by = request.auth
    project.save()
    return project


@router.post("/project-search", response={201:List[ProjectSchema]}, auth=AuthBearer(), tags=['Project'])
@paginate
def get_projects(request, payload: QuerySchema):
    """
    Retrieves a list of projects based on the provided query parameters.

    Parameters:
    request (Request): The incoming request object.

    Returns:
    List[ProjectSchema]: A list of project objects. If no query parameters are provided, all projects are returned.
    """
    payload_dict = payload.dict()
    filter_q = Q()
    sort_value = '-created_at'
    if payload_dict.get('filters'):
        filter_q = Q(**payload_dict['filters'])

    if payload_dict.get('sort'):
        sort_value = payload_dict['sort']

    container_data = Project.objects.filter(filter_q).order_by(sort_value)
    return container_data

@router.get("/project-by-code/{code}", response={200:ProjectSchema}, auth=AuthBearer(), tags=['Project'])
def get_project_by_code(request, code):
    """
    Retrieves a project object based on the provided project code.

    Parameters:
    request (Request): The incoming request object.
    code (str): The unique code of the project to be retrieved.

    Returns:
    Project: The project object with the matching code. If no project is found, a 404 Not Found error is raised.
    """
    project = get_object_or_404(Project, code=code)
    return project

# -------------------------------- Containers --------------------------------

@router.post("/container", response={201: ContainerSchema}, auth=AuthBearer(), tags=['Container'])
def create_container(request, payload: ContainerInSchema):
    """
    Creates a new container in the system.

    Parameters:
    request (Request): The incoming request object.
    payload (ContainerSchema): The container data to be created. This includes the project and container type IDs.

    Returns:
    tuple: A tuple containing the HTTP status code and the created container object.
           If an error occurs during the creation process, a 400 status code and an error message are returned.
    """
    project = get_object_or_404(Project, id=payload.project)
    container_type = get_object_or_404(ContainerType, id=payload.container_type)
    payload_dict = payload.dict()
    payload_dict['project'] = project
    payload_dict['container_type'] = container_type
    ctr = Container.objects.create(**payload_dict)
    ctr.created_by = request.auth
    ctr.modified_by = request.auth
    ctr.save()
    return 201, ctr


@router.patch("/container/{uid}", response={200:ContainerSchema}, auth=AuthBearer(), tags=['Container'])
def update_container(request, uid: str, payload: ContainerSchema):
    """
    Updates an existing container in the system.

    Parameters:
    request (Request): The incoming request object.
    uid (str): The unique identifier of the container to be updated.
    payload (ContainerSchema): The updated container data. This includes the project and container type IDs.

    Returns:
    Container: The updated container object.
    """
    ctr = get_object_or_404(Container, id=uid)
    ctr.client_name = payload.client_name
    ctr.frame_range = payload.frame_range
    ctr.modified_by = request.auth
    ctr.save()
    return ctr


@router.post("/container-search", response={201:List[ContainerSchema]}, auth=AuthBearer(), tags=['Container'])
@paginate
def get_containers(request, payload: QuerySchema):
    """
    Retrieves a list of containers based on the provided query parameters.

    Parameters:
    request (Request): The incoming request object.

    Returns:
    List[ContainerSchema]: A list of container objects. If no query parameters are provided, all containers are returned.
    """
    payload_dict = payload.dict()
    filter_q = Q()
    sort_value = '-created_at'
    if payload_dict.get('filters'):
        filter_q = Q(**payload_dict['filters'])

    if payload_dict.get('sort'):
        sort_value = payload_dict['sort']

    container_data = Container.objects.filter(filter_q).order_by(sort_value)
    return container_data

@router.get("/container-by-code/{code}", response={200:ContainerSchema}, auth=AuthBearer(), tags=['Container'])
def get_container_by_code(request, code):
    """
    Retrieves a container object based on the provided container code.

    Parameters:
    request (Request): The incoming request object.
    code (str): The unique code of the container to be retrieved.

    Returns:
    Container: The container object with the matching code. If no container is found, a 404 Not Found error is raised.
    """
    container = get_object_or_404(Container, code=code)
    return container

# -------------------------------- Container Relation --------------------------------

@router.post("/container-relation", response={201: ContainerRelationSchemaOut}, auth=AuthBearer(), tags=['Container Relation'])
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
    relationship_obj.created_by = request.auth
    relationship_obj.modified_by = request.auth
    relationship_obj.save()
    return 201, relationship_obj


@router.patch("/container-relation/{uid}", response={200: ContainerRelationSchemaOut}, auth=AuthBearer(), tags=['Container Relation'])
def update_container_realtion(request, uid, payload: ContainerRelationSchema):
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
    relationship_obj.modified_by = request.auth
    relationship_obj.save()
    return relationship_obj


@router.get("/container-relation/{cid}/{rid}", response={200: List[ContainerRelationSchemaOut]}, auth=AuthBearer(), tags=['Container Relation'])
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

# -------------------------------- Product --------------------------------

@router.post("/product", response={201: ProductSchema}, auth=AuthBearer(), tags=['Product'])
def create_product(request, payload: ProductInSchema):
    """
    Creates a new product in the system.

    Parameters:
    request (Request): The incoming request object.
    payload (ProductSchema): The product data to be created. This includes the container, step, data_type, element IDs.

    Returns:
    tuple: A tuple containing the HTTP status code and the created product object.
           If an error occurs during the creation process, a 400 status code and an error message are returned.
    """
    payload_dict = payload.dict()
    payload_dict['container'] = get_object_or_404(Container, id=payload.container)
    payload_dict['step'] = get_object_or_404(Step, id=payload.step)
    payload_dict['data_type'] = get_object_or_404(DataType, id=payload.data_type)
    payload_dict['status'] = get_object_or_404(Status, code='rgsr')
    payload_dict['element'] = get_object_or_404(Element, id=payload.element)
    prod = Product.objects.create(**payload_dict)
    prod.created_by = request.auth
    prod.modified_by = request.auth
    prod.save()
    return 201, prod


@router.post("/product-search", response={201:List[ProductSchema]}, auth=AuthBearer(), tags=['Product'])
@paginate
def get_products(request, payload: QuerySchema):
    """
    Retrieves a list of products based on the provided query parameters.

    Parameters:
    request (Request): The incoming request object.

    Returns:
    List[ProductSchema]: A list of product objects. If no query parameters are provided, all products are returned.
    """
    payload_dict = payload.dict()
    filter_q = Q()
    sort_value = '-created_at'
    if payload_dict.get('filters'):
        filter_q = Q(**payload_dict['filters'])

    if payload_dict.get('sort'):
        sort_value = payload_dict['sort']

    product_data = Product.objects.filter(filter_q).order_by(sort_value)
    return product_data


@router.patch("/product/{uid}", response={200:ProductSchema}, auth=AuthBearer(), tags=['Product'])
def update_product(request, uid: str, payload: ProductSchema):
    """
    Updates an existing product in the system.

    Parameters:
    request (Request): The incoming request object.
    uid (str): The unique identifier of the product to be updated.
    payload (ProductSchema): The updated product data. This includes the filepath, frame_range, extension, tasks, metadata.

    Returns:
    Product: The updated product object.
    """
    product = get_object_or_404(Product, id=uid)
    editables = ['filepath','frame_range','extension','tasks','metadata']
    for attr, value in payload.dict().items():
        if attr in editables:
            setattr(product, attr, value)
    product.modified_by = request.auth
    product.save()
    return product


@router.patch("/product/{uid}/{status}", response={200:ProductSchema}, auth=AuthBearer(), tags=['Product'])
def set_status(request, uid: str, status: str):
    """
    Updates the status of an existing product in the system.

    Parameters:
    request (Request): The incoming request object.
    uid (str): The unique identifier of the product to be updated.
    status (str): The new status code for the product.

    Returns:
    Product: The updated product object.
    """
    product = get_object_or_404(Product, id=uid)
    status = get_object_or_404(Status, code=status)
    product.status = status
    product.modified_by = request.auth
    if status.code == 'appr':
        product.approved_by = request.auth
        product.approved_at = timezone.now()
    product.save()
    return product

# -------------------------------- Product Dependency --------------------------------

@router.post("/product-dependency", response={201: ProductDependencySchema}, auth=AuthBearer(), tags=['Product Dependency'])
def created_product_dependency(request, payload: ProductDependencySchemaIn):
    """
    Creates a new product dependency in the system.

    Parameters:
    request (Request): The incoming request object.
    payload (ProductDependencySchemaIn): The product dependency data to be created. This includes the product ID and a list of dependency filepaths.

    Returns:
    tuple: A tuple containing the HTTP status code (201) and the created product dependency object.
    """
    product = get_object_or_404(Product, id=payload.product)
    dependencies = Product.objects.filter(filepath__in=payload.dependencies)
    dep_obj = ProductDependency.objects.create(product=product)
    dep_obj.dependencies.set(dependencies)
    dep_obj.created_by = request.auth
    dep_obj.modified_by = request.auth
    dep_obj.save()
    return 201, dep_obj


@router.get("/product-dependency/{uid}", response={200: ProductDependencySchema}, auth=AuthBearer(), tags=['Product Dependency'])
def get_product_dependency(request, uid):
    """
    Retrieves a product dependency object based on the provided unique identifier.

    Parameters:
    request (Request): The incoming request object.
    uid (str): The unique identifier of the product dependency to be retrieved.

    Returns:
    ProductDependency: The product dependency object with the matching unique identifier.
    """
    product_obj = get_object_or_404(Product, id=uid)
    dep_obj = get_object_or_404(ProductDependency, product=product_obj)
    return 200, dep_obj

# -------------------------------- Bundle --------------------------------

@router.post("/bundle", response={201: BundleSchemaOut}, auth=AuthBearer(), tags=['Bundle'])
def create_bundle(request, payload: BundleSchema):
    """
    Creates a new bundle in the system.

    Parameters:
    request (Request): The incoming request object.
    payload (BundleSchema): The bundle data to be created. This includes the container, bundle type IDs, and product IDs.

    Returns:
    tuple: A tuple containing the HTTP status code (201) and the created bundle object.
           If an error occurs during the creation process, a 400 status code and an error message are returned.
    """
    payload_dict = {}
    payload_dict['container'] = get_object_or_404(Container, id=payload.container)
    payload_dict['step'] = get_object_or_404(Step, id=payload.step)
    payload_dict['bundle_type'] = get_object_or_404(BundleType, id=payload.bundle_type)
    payload_dict['status'] = get_object_or_404(Status, code='rgsr')
    bdl = Bundle.objects.create(**payload_dict)
    products = Product.objects.filter(id__in=payload.products)
    bdl.products.set(products)
    bdl.created_by = request.auth
    bdl.modified_by = request.auth
    bdl.save()
    return 201, bdl

@router.patch("/bundle/{uid}", response={200: BundleSchemaOut}, auth=AuthBearer(), tags=['Bundle'])
def update_bundle(request, uid, payload: BundleSchema):
    """
    Updates an existing relationship between containers.

    Parameters:
    request (Request): The incoming request object.
    uid (str): The unique identifier of the relationship to be updated.
    payload (ContainerRelationSchema): The updated relationship data. This includes the IDs of the to_containers.

    Returns:
    ContainerRelation: The updated relationship object.
    """
    bdl = get_object_or_404(Bundle, id=uid)
    products = Product.objects.filter(id__in=payload.products)
    bdl.products.set(products)
    bdl.modified_by = request.auth
    bdl.save()
    return 200, bdl

@router.post("/bundle-search", response={201: List[BundleSchemaOut]}, auth=AuthBearer(), tags=['Bundle'])
@paginate
def get_bundles(request, payload: QuerySchema):
    payload_dict = payload.dict()
    filter_q = Q()
    sort_value = '-created_at'
    if payload_dict.get('filters'):
        filter_q = Q(**payload_dict['filters'])

    if payload_dict.get('sort'):
        sort_value = payload_dict['sort']
        
    product_data = Bundle.objects.filter(filter_q).order_by(sort_value)
    return product_data
