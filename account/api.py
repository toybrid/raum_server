import os
from typing import List
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db.models import Q
from ninja import Router
from .schemas import UserSchema, UserSchemaOut, TokenSchema, LoginSchema
from ams.schemas import QuerySchema
from .import utils
from account.models import User
from account.utils import AuthBearer
from ninja.pagination import paginate

router = Router()

@router.post("/register-user", response={201: UserSchemaOut}, tags=['auth'])
def register(request, user_data: UserSchema):
    """
    Registers a new user with the provided data.

    Parameters:
    request (Request): The incoming request object.
    user_data (UserSchema): The user data to be registered.

    Returns:
    dict: A dictionary containing an 'Error' message if the email domain is invalid.
    tuple: A tuple containing the HTTP status code (201) and the created user object if the email domain is valid.
    """
    if utils.verify_email_domains(user_data.email):
        user = User.objects.create(
            username=user_data.username,
            email=user_data.email,
            password=make_password(user_data.password),
            first_name= user_data.first_name if user_data.first_name else '',
            last_name=user_data.last_name if user_data.last_name else '',
            is_staff=False,
            is_superuser=False,
            is_active=True,
        )
        artist_group = get_object_or_404(Group, name='artist')
        user.save()
        user.groups.add(artist_group)
        user.save()
        return 201, user
    return {'Error':'Invalid email domain'}

@router.post("/login", response={200: TokenSchema}, tags=['auth'])
def login(request, payload: LoginSchema):
    """
    Authenticates a user with the provided email and password.

    Parameters:
    request (Request): The incoming request object.
    payload (LoginSchema): The login payload containing email and password.

    Returns:
    TokenSchema: The generated token if the user is authenticated.
    """
    user = authenticate(email=payload.email, password=payload.password)
    if user:
        token = utils.get_or_create_token(user)
        return token

@router.post("/get-users", response={201:List[UserSchemaOut]}, auth=AuthBearer(), tags=['User'])
@paginate
def get_users(request, payload: QuerySchema):
    """
    Retrieves a list of users based on the provided query parameters.

    Parameters:
    request (Request): The incoming request object.

    Returns:
    List[UserSchemaOut]: A list of user objects based on the query parameters.
    """
    payload_dict = payload.dict()
    filter_q = Q()
    sort_value = None
    if payload_dict.get('filters'):
        filter_q = Q(**payload_dict['filters'])

    if payload_dict.get('sort'):
        sort_value = payload_dict['sort']

    container_data = User.objects.filter(filter_q).order_by(sort_value)
    return container_data