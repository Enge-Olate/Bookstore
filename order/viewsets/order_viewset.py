from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from ..models import Order
from ..serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    for user in User.objects.all():
        Token.objects.get_or_create(user=user)
