from rest_framework.serializers import ModelSerializer
from rest_framework_gis.serializers import GeoModelSerializer
from .models import *

class UserSerializer(GeoModelSerializer):
    class Meta:
        model = User
        exclude = ['last_login', 'is_superuser', 'password', 'is_active', 'is_admin', 'is_staff', 'groups', 'user_permissions']
        
class UserAdminSerializer(GeoModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UserSignUpSerializer(GeoModelSerializer):
    class Meta:
        model = User
        exclude = ['last_login', 'is_superuser', 'is_active', 'is_admin', 'is_staff', 'groups', 'user_permissions']
        
class WorkDistanceSerializer(GeoModelSerializer):
    class Meta:
        model = WorkDistance
        fields = '__all__'
        
class AreaOfInterestSerializer(GeoModelSerializer):
    class Meta:
        model = AreaOfInterest
        fields = '__all__'
        
class DocumentSerializer(GeoModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'