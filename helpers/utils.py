import os
from django.db.models import Q
from helpers.constants import BUILTIN_QUERY_PARAMS
from dotenv import load_dotenv

load_dotenv()

def get_allowed_hosts():
    """
    Retrieves the list of allowed hosts from the environment variable 'RAUM_ALLOWED_HOSTS'.

    The function retrieves the value of the 'RAUM_ALLOWED_HOSTS' environment variable,
    splits it by commas, and returns a list of the resulting domain names.

    Parameters:
    None

    Returns:
    list: A list of domain names extracted from the 'RAUM_ALLOWED_HOSTS' environment variable.
    """
    allowd_hosts = os.getenv('RAUM_ALLOWED_HOSTS', None)
    domain_list = allowd_hosts.split(",")
    return domain_list


def generic_get(model_object, payload):
    """
    This function performs a generic get operation on a Django model object based on the provided payload.

    Parameters:
    model_object (Django Model): The Django model object on which the get operation will be performed.
    payload (Pydantic Model): The payload containing filter and sort parameters.

    Returns:
    QuerySet: A Django QuerySet containing the filtered and sorted data from the model object.

    The function extracts the filter and sort parameters from the payload. If filter parameters are present,
    it constructs a Q object using these parameters and applies it to the model object's filter method.
    If sort parameters are present, it orders the resulting QuerySet based on these parameters.
    """
    payload_dict = payload.dict()
    filter_q = Q()

    if payload_dict.get('filters'):
        filter_q = Q(**payload_dict['filters'])

    if payload_dict.get('sort'):
        sort_value = payload_dict['sort']

    container_data = model_object.objects.filter(filter_q).order_by(*sort_value)
    return container_data

def generic_get_with_prefetch(model_object, prefetch_list, payload):
    """
    Performs a generic get operation on a Django model object with prefetching related objects,
    based on the provided payload.

    Parameters:
    model_object (Django Model): The Django model object on which the get operation will be performed.
    prefetch_list (list): A list of related objects to be prefetched using Django's prefetch_related method.
    payload (Pydantic Model): The payload containing filter and sort parameters.

    Returns:
    QuerySet: A Django QuerySet containing the filtered, sorted, and prefetched data from the model object.

    The function extracts the filter and sort parameters from the payload. If filter parameters are present,
    it constructs a Q object using these parameters and applies it to the model object's filter method.
    If sort parameters are present, it orders the resulting QuerySet based on these parameters.
    The function also uses Django's prefetch_related method to fetch related objects specified in the prefetch_list.
    """
    payload_dict = payload.dict()
    filter_q = Q()
    if payload_dict.get('filters'):
        filter_q = Q(**payload_dict['filters'])

    if payload_dict.get('sort'):
        sort_value = payload_dict['sort']

    container_data = model_object.objects.prefetch_related(*prefetch_list).filter(filter_q).order_by(*sort_value)
    return container_data