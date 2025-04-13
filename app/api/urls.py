from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParkViewSet


router = DefaultRouter()
router.register(r'parks', ParkViewSet, basename='park')

urlpatterns = [
    path('api/', include(router.urls)), 
]
