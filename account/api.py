import os
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from ninja import Router
from .schemas import UserSchema, UserSchemaOut, TokenSchema, LoginSchema
from helpers.schemas import ErrorSchema
from .import utils
from account.models import User

router = Router()

@router.post("/register-user", response={201: UserSchemaOut}, tags=['auth'])
def register(request, user_data: UserSchema):
    print(user_data)
    if utils.verify_email_domains(user_data.email):
        print('----------------------------------------------------------------')
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
    user = authenticate(email=payload.email, password=payload.password)
    if user:
        token = utils.get_or_create_token(user)
        return token