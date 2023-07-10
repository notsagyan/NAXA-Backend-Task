from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import *
from .models import *
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.contrib.auth.password_validation import validate_password
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ObjectDoesNotExist

def custom_validate_password(password: str) -> Response|None:
    try:
        validate_password(password)
    except Exception as ex:
        return Response(ex, status = status.HTTP_400_BAD_REQUEST)

class StandardPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    pagination_class = StandardPagination


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if request.user.has_perm('authentication.add_user'):
            res = custom_validate_password(request.data['password'])
            if res:
                return res
            return super().create(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()
        
        
class UserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.user.is_admin or self.request.user.is_superuser:
            return UserAdminSerializer
        return UserSerializer
    
    def retrieve(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.view_user')) or (request.user == self.get_object()):
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def update(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.change_user')) or (request.user == self.get_object()):
            if 'password' in request.data:
                res = custom_validate_password(request.data['password'])
                if res:
                    return res
            return super().update(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def perform_update(self, serializer) -> None:
        instance = serializer.save()
        if 'password' in self.request.data:
            instance.set_password(instance.password)
            instance.save()
        
    def destroy(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.delete_user')) or (request.user == self.get_object()):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def patch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.change_user')) or (request.user == self.get_object()):
            if 'password' in request.data:
                res = custom_validate_password(request.data['password'])
                if res:
                    return res
            return super().patch(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
        
class UserSignupView(APIView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        serializer = UserSignUpSerializer(data = request.data)
        password = request.data['password']
        
        if serializer.is_valid():
            user = serializer.save()
            res = custom_validate_password(request.data['password'])
            if res:
                return res
            user.set_password(password)
            user.save()
            
            return Response('User created successfully.', status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
class UserFindView(APIView):
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        point = Point(request.data['latitude'], request.data['longitude'])
        instance = User.objects.filter(
            home_address__distance_lt = (point, Distance(km = 10))
        )
        users = UserSerializer(data = instance, many = True).data
        return Response(
            users,
            status = status.HTTP_200_OK
        )
        
        
class WorkDistanceView(ModelViewSet):
    queryset = WorkDistance.objects.all()
    serializer_class = WorkDistanceSerializer
    pagination_class = StandardPagination
    
    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        user_id = request.query_params.get('user', None)
        try:
            user = User.objects.get(id = user_id)
        except ObjectDoesNotExist:
            return Response('User not found', status = status.HTTP_404_NOT_FOUND)
        else:
            if (request.user.has_perm('authentication.view_workdistance')) or (request.user.id == user):
                work_distance_list = WorkDistance.objects.filter(user = user)
                serializer = WorkDistanceSerializer(work_distance_list, many = True)
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_403_FORBIDDEN)
        
    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.add_workdistance')) or (request.user.id == self.get_object().user):
            return super().create(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def retrieve(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.view_workdistance')) or (request.user.id == self.get_object().user):
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def update(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.change_workdistance')) or (request.user.id == self.get_object().user):
            return super().update(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def destroy(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.delete_workdistance')) or (request.user.id == self.get_object().user):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        

class AreaOfInterestView(ModelViewSet):
    queryset = AreaOfInterest.objects.all()
    serializer_class = AreaOfInterestSerializer
    pagination_class = StandardPagination
    
    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        user_id = request.query_params.get('user', None)
        try:
            user = User.objects.get(id = user_id)
        except ObjectDoesNotExist:
            return Response('User not found', status = status.HTTP_404_NOT_FOUND)
        else:
            if (request.user.has_perm('authentication.view_areaofinterest')) or (request.user.id == user):
                aof_list = AreaOfInterest.objects.filter(user = user)
                serializer = AreaOfInterestSerializer(aof_list, many = True)
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_403_FORBIDDEN)
        
    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.add_areaofinterest')) or (request.user.id == self.get_object().user):
            return super().create(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def retrieve(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.view_areaofinterest')) or (request.user.id == self.get_object().user):
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def update(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.change_areaofinterest')) or (request.user.id == self.get_object().user):
            return super().update(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def destroy(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.delete_areaofinterest')) or (request.user.id == self.get_object().user):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
        
class DocumentView(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    pagination_class = StandardPagination
    permission_classes = [IsAuthenticated]
    
    def list(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        user_id = request.query_params.get('user', None)
        try:
            user = User.objects.get(id = user_id)
        except ObjectDoesNotExist:
            return Response('User not found', status = status.HTTP_404_NOT_FOUND)
        else:
            if (request.user.has_perm('authentication.view_document')) or (request.user.id == user):
                document_list = Document.objects.filter(user = user)
                serializer = DocumentSerializer(document_list, many = True)
                return Response(serializer.data, status = status.HTTP_200_OK)
            else:
                return Response(status = status.HTTP_403_FORBIDDEN)
        
    def create(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.add_document')) or (request.user.id == request.data['user']):
            return super().create(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def retrieve(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.view_document')) or (request.user.id == self.get_object().user):
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def update(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.change_document')) or (request.user.id == self.get_object().user):
            return super().update(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def destroy(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.delete_document')) or (request.user.id == self.get_object().user):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)