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

@router.get("/bearer", auth=utils.AuthBearer(), tags=['auth'])
def bearer(request):
    return {"token": request.auth}

@router.post("/register-user", response={201: UserSchemaOut, 400: ErrorSchema}, tags=['auth'], include_in_schema=False)
def register(request, user_data: UserSchema):
    if utils.verify_email_domains(user_data.email):
        try:
            user = User(
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
        except Exception as e:
            return 400, {'message': str(e)}
    else:
        return 400, {"message": "Invalid email domain"}

@router.post("/login", response={200: TokenSchema, 400: ErrorSchema}, tags=['auth'])
def login(request, payload: LoginSchema):
    user = authenticate(email=payload.email, password=payload.password)
    if user:
        token = utils.get_or_create_token(user)
        return 200, token
    return 400, {"error": "Invalid credentials"}