import os
from django.db.models import Q
from helpers.constants import BUILTIN_QUERY_PARAMS
from dotenv import load_dotenv

load_dotenv()

def get_allowed_hosts():
    allowd_hosts = os.getenv('RAUM_ALLOWED_HOSTS', None)
    domain_list = allowd_hosts.split(",")
    return domain_list


def generic_get(model_object, payload):
    payload_dict = payload.dict()
    filter_q = Q()

    if payload_dict.get('filters'):
        filter_q = Q(**payload_dict['filters'])

    if payload_dict.get('sort'):
        sort_value = payload_dict['sort']

    container_data = model_object.objects.filter(filter_q).order_by(*sort_value)
    return container_data

def generic_get_with_prefetch(model_object, prefetch_list, payload):
    payload_dict = payload.dict()
    filter_q = Q()
    if payload_dict.get('filters'):
        filter_q = Q(**payload_dict['filters'])

    if payload_dict.get('sort'):
        sort_value = payload_dict['sort']

    container_data = model_object.objects.prefetch_related(*prefetch_list).filter(filter_q).order_by(*sort_value)
    return container_data