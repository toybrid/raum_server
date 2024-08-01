from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate
from typing import List
from core.models import ContainerType, Status, Element, DataType, Step, RelationType
from core.schemas import ContainerTypeSchema, StatusSchema, ElementSchema, DataTypeSchema, StepSchema, RelationTypeSchema
from helpers.utils import build_filters
from account.utils import AuthBearer


router = Router()

@router.get("/container-type", response={200:List[ContainerTypeSchema]}, auth=AuthBearer(), tags=['core'])
@paginate
def get_container_types(request):
    """
    Retrieve a list of ContainerType objects.

    This function retrieves all ContainerType objects from the database or filters them based on the provided query parameters.

    Parameters:
    request (Request): The request object containing the query parameters.

    Returns:
    QuerySet: A QuerySet of ContainerType objects.
    """
    query_params = build_filters(request.GET)
    if query_params:
        return ContainerType.objects.filter(**query_params)
    return ContainerType.objects.all()

@router.get("/container-type-by-code/{code}", response={200:ContainerTypeSchema}, auth=AuthBearer(), tags=['core'])
def get_container_type_by_code(request, code):
    """
    Retrieve a single ContainerType object by its code.

    This function retrieves a single ContainerType object from the database based on the provided code.

    Parameters:
    request (Request): The request object.
    code (str): The code of the ContainerType object to retrieve.

    Returns:
    ContainerType: The requested ContainerType object.
    """
    container_type = get_object_or_404(ContainerType, code=code)
    return container_type

@router.get("/status", response={200:List[StatusSchema]}, auth=AuthBearer(), tags=['core'])
@paginate
def get_statuses(request):
    """
    Retrieve a list of Status objects.

    This function retrieves all Status objects from the database or filters them based on the provided query parameters.

    Parameters:
    request (Request): The request object containing the query parameters.

    Returns:
    QuerySet: A QuerySet of Status objects.
    """
    query_params = build_filters(request.GET)
    if query_params:
        return Status.objects.filter(**query_params)
    return Status.objects.all()

@router.get("/element", response={200:List[ElementSchema]}, auth=AuthBearer(), tags=['core'])
@paginate
def get_elements(request):
    """
    Retrieve a list of Element objects.

    This function retrieves all Element objects from the database or filters them based on the provided query parameters.

    Parameters:
    request (Request): The request object containing the query parameters.

    Returns:
    QuerySet: A QuerySet of Element objects.
    """
    query_params = build_filters(request.GET)
    if query_params:
        return Element.objects.filter(**query_params)
    return Element.objects.all()

@router.get("/data-type", response={200:List[DataTypeSchema]}, auth=AuthBearer(), tags=['core'])
@paginate
def get_data_types(request):
    """
    Retrieve a list of DataType objects.

    This function retrieves all DataType objects from the database or filters them based on the provided query parameters.

    Parameters:
    request (Request): The request object containing the query parameters.

    Returns:
    QuerySet: A QuerySet of DataType objects.
    """
    query_params = build_filters(request.GET)
    if query_params:
        return DataType.objects.filter(**query_params)
    return DataType.objects.all()

@router.get("/step", response={200:List[StepSchema]}, auth=AuthBearer(), tags=['core'])
@paginate
def get_steps(request):
    """
    Retrieve a list of Step objects.

    This function retrieves all Step objects from the database or filters them based on the provided query parameters.

    Parameters:
    request (Request): The request object containing the query parameters.

    Returns:
    QuerySet: A QuerySet of Step objects.
    """
    query_params = build_filters(request.GET)
    if query_params:
        return Step.objects.filter(**query_params)
    return Step.objects.all()

@router.get("/relation-type", response={200:List[RelationTypeSchema]}, auth=AuthBearer(), tags=['core'])
@paginate
def get_relation_types(request):
    """
    Retrieve a list of RelationType objects.

    This function retrieves all RelationType objects from the database or filters them based on the provided query parameters.

    Parameters:
    request (Request): The request object containing the query parameters.

    Returns:
    QuerySet: A QuerySet of RelationType objects.
    """
    query_params = build_filters(request.GET)
    if query_params:
        return RelationType.objects.filter(**query_params)
    return RelationType.objects.all()