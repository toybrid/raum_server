from ninja import ModelSchema, Schema
from account.models import User, AuthUserToken

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        fields_optional = '__all__'

class UserSchemaOut(ModelSchema):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        fields_optional = '__all__'

class LoginSchema(Schema):
    email: str
    password: str

class TokenSchema(ModelSchema):
    class Meta:
        model = AuthUserToken
        fields = ['id', 'expires_at']
        fields_optional = '__all__'