from rest_framework import viewsets
from ..models import Product
from ..serializers import ProductSerializer

class ProdutViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    