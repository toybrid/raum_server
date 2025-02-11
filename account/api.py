import os
from typing import List
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.db.models import Q
from ninja import Router
from .schemas import UserSchema, UserSchemaOut, TokenSchema, LoginSchema
from helpers.schemas import QuerySchema
from .import utils
from helpers.utils import generic_get
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
    return generic_get(User, payload)

@router.get("/is-authorised", auth=AuthBearer(), tags=['User'])
def is_authorised(request):
    """
    Checks if the user is authorised to access the API.

    Parameters:
    request (Request): The incoming request object.

    Returns:
    bool: True if the user is authorised, False otherwise.
    """
    return request.auth.username
