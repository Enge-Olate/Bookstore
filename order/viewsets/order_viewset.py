from rest_framework.viewsets import ModelViewset

from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(ModelViewset):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
