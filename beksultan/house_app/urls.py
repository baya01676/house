from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileListAPIView,UserProfileDetailAPIView,
    PropertDetailAPIView,PropertyListAPIView,
    PropertyImageViewSet,
    PropertyDocumentViewSet,
    ReviewViewSet,
    DistrictViewSet,
    CityDetailAPIView,CityListAPIView,LoginView,RegisterView,LogoutView
)

router = DefaultRouter()
router.register(r'property-images', PropertyImageViewSet)
router.register(r'property-documents', PropertyDocumentViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'district',DistrictViewSet)

urlpatterns = [
   path('', include(router.urls)),
    path('property',PropertyListAPIView.as_view(),name='property_list'),
    path('property<int:pk>/',PropertDetailAPIView.as_view(),name='property_detail'),
    path('users', UserProfileListAPIView.as_view(), name='users_list'),
    path('users/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('city',CityListAPIView.as_view(),name='city_list'),
    path('city/<int:pk>/',CityDetailAPIView.as_view(),name='city_detail'),
    path('login',LoginView.as_view(),name='login'),
    path('register',RegisterView.as_view(),name='register'),
    path('logout',LogoutView.as_view(),name='logout')
]