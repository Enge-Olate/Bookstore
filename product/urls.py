from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets.product_viewset import ProdutViewSet

router = DefaultRouter()
router.register(r'product', ProdutViewSet, basename='product')

urlpatterns =[
    path('', include(router.urls))
]