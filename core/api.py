from ninja import Router
from ninja.pagination import paginate
from typing import List
from core.models import ContainerType, Status, Element, DataType, Step, RelationType, BundleType
from core.schemas import ContainerTypeSchema, StatusSchema, ElementSchema, DataTypeSchema, StepSchema, RelationTypeSchema, BundleTypeSchema
from ams.schemas import QuerySchema
from helpers.utils import generic_get
from account.utils import AuthBearer


router = Router()

@router.post("/container-type", response={201:List[ContainerTypeSchema]}, auth=AuthBearer(), tags=['core'])
@paginate
def get_container_types(request, payload: QuerySchema):
    """
    Retrieve a list of ContainerType objects.

    This function retrieves all ContainerType objects from the database or filters them based on the provided query parameters.

    Parameters:
    request (Request): The request object containing the query parameters.

    Returns:
    QuerySet: A QuerySet of ContainerType objects.
    """
    return generic_get(ContainerType, payload)


@router.post("/status", response={201:List[StatusSchema]}, auth=AuthBearer(), tags=['core'])
@paginate
def get_statuses(request, payload: QuerySchema):
    """
    Retrieve a list of Status objects.

    This function retrieves all Status objects from the database or filters them based on the provided query parameters.

    Parameters:
    request (Request): The request object containing the query parameters.

    Returns:
    QuerySet: A QuerySet of Status objects.
    """
    return generic_get(Status, payload)

@router.post("/element", response={201:List[ElementSchema]}, auth=AuthBearer(), tags=['core'])
@paginate
def get_elements(request, payload: QuerySchema):
    """
    Retrieve a list of Element objects.

    This function retrieves all Element objects from the database or filters them based on the provided query parameters.

    Parameters:
    request (Request): The request object containing the query parameters.

    Returns:
    QuerySet: A QuerySet of Element objects.
    """
    return generic_get(Element, payload)

@router.post("/data-type", response={201:List[DataTypeSchema]}, auth=AuthBearer(), tags=['core'])
@paginate
def get_data_types(request, payload: QuerySchema):
    """
    Retrieve a list of DataType objects.

    This function retrieves all DataType objects from the database or filters them based on the provided query parameters.

    Parameters:
    request (Request): The request object containing the query parameters.

    Returns:
    QuerySet: A QuerySet of DataType objects.
    """
    return generic_get(DataType, payload)

@router.post("/step", response={201:List[StepSchema]}, auth=AuthBearer(), tags=['core'])
@paginate
def get_steps(request, payload: QuerySchema):
    """
    Retrieve a list of Step objects.

    This function retrieves all Step objects from the database or filters them based on the provided query parameters.

    Parameters:
    request (Request): The request object containing the query parameters.

    Returns:
    QuerySet: A QuerySet of Step objects.
    """
    return generic_get(Step, payload)

@router.post("/relation-type", response={201:List[RelationTypeSchema]}, auth=AuthBearer(), tags=['core'])
@paginate
def get_relation_types(request, payload: QuerySchema):
    """
    Retrieve a list of RelationType objects.

    This function retrieves all RelationType objects from the database or filters them based on the provided query parameters.

    Parameters:
    request (Request): The request object containing the query parameters.

    Returns:
    QuerySet: A QuerySet of RelationType objects.
    """
    return generic_get(RelationType, payload)

@router.post("/bundle-type", response={201:List[BundleTypeSchema]}, auth=AuthBearer(), tags=['core'])
@paginate
def get_bundle_types(request, payload: QuerySchema):
    """
    Retrieve a list of RelationType objects.

    This function retrieves all RelationType objects from the database or filters them based on the provided query parameters.

    Parameters:
    request (Request): The request object containing the query parameters.

    Returns:
    QuerySet: A QuerySet of RelationType objects.
    """
    return generic_get(BundleType, payload)