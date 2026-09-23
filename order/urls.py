from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.order_viewset import OrderViewSet

router = DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')

urlpatterns =[
    path('', include(router.urls))
]