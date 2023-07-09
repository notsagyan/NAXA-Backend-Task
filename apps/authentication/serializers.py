from rest_framework.serializers import ModelSerializer
from .models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['last_login', 'is_superuser', 'password', 'is_active', 'is_admin', 'is_staff', 'groups', 'user_permissions']
        
class UserAdminSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UserSignUpSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['last_login', 'is_superuser', 'is_active', 'is_admin', 'is_staff', 'groups', 'user_permissions']