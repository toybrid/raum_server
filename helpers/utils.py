import os
from helpers.constants import BUILTIN_QUERY_PARAMS
from dotenv import load_dotenv

load_dotenv()

def build_filters(query_parms):
    query_dict = query_parms.dict()
    for i in BUILTIN_QUERY_PARAMS:
        if i in query_dict:
            query_dict.pop(i)
    return query_dict

def get_allowed_hosts():
    allowd_hosts = os.getenv('RAUM_ALLOWED_HOSTS', None)
    domain_list = allowd_hosts.split(",")
    return domain_list