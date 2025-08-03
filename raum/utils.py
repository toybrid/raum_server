import os

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