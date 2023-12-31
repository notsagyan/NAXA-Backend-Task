from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import *
from rest_framework.routers import SimpleRouter

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    
    path('api/user/list/', UserListView.as_view(), name = 'api-user-list'),
    path('api/user/create/', UserCreateView.as_view(), name = 'api-user-create'),
    path('api/user/<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name = 'api-user-rud'),
    path('api/user/signup/', UserSignupView.as_view(), name = 'api-signup'),
    path('api/user/find/', UserFindView.as_view(), name = 'api-user-find')
]

router = SimpleRouter()
router.register('api/user/work-distance', WorkDistanceView)
router.register('api/user/area-interest', AreaOfInterestView)
router.register('api/user/document', DocumentView)
urlpatterns += router.urls