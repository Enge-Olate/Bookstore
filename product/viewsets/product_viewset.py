from rest_framework.viewsets import ModelViewSet
from ..models import Product
from ..serializers import ProductSerializer

class ProdutViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    