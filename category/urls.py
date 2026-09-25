from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.category_viewset import CategoryViewSet

router = DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')

urlpatterns =[
    path('', include(router.urls))
]