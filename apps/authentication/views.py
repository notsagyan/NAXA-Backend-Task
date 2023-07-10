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
            return super().create(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
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
            return super().update(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def destroy(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.delete_user')) or (request.user == self.get_object()):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
    def patch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        if (request.user.has_perm('authentication.change_user')) or (request.user == self.get_object()):
            return super().patch(request, *args, **kwargs)
        else:
            return Response(status = status.HTTP_403_FORBIDDEN)
        
class UserSignupView(APIView):
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> Response:
        serializer = UserSignUpSerializer(data = request.data)
        password = request.data['password']
        
        if serializer.is_valid():
            user = serializer.save()
            
            # Validate password.
            try:
                validate_password(password)
            except Exception as ex:
                print(ex)
                return Response(ex, status = status.HTTP_400_BAD_REQUEST)
            
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