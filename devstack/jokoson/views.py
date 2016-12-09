from django.shortcuts import render
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse

from jokoson.models import Equip, Order, Vendor, Gpssensor, Gpsdata, Category, UploadFile
from jokoson.serializers import EquipSerializer, OrderSerializer, \
    UserSerializer, VendorSerializer, GpssensorSerializer, GpsdataSerializer, CategorySerializer, \
    UploadFileSerializer
from jokoson.permissions import IsOwnerOrReadOnly

MODELS = ['user', 'order', 'equip','vendor', 'gpssensor', 'gpsdata', 'category']

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
def api_root(request, format=None):
    mapship = {}
    for model in MODELS:
        key = model 
        value =  reverse('%s-list'%model, request=request, format=format)
        mapship[key] = value
    return Response(mapship)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('')

    def get_queryset(self):
        queryset = Order.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            queryset = queryset.filter(buyer__username=username)
        return queryset

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)


class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class EquipList(generics.ListCreateAPIView):
    queryset = Equip.objects.all()
    serializer_class = EquipSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class EquipDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Equip.objects.all()
    serializer_class = EquipSerializer


class VendorList(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class VendorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class GpssensorList(generics.ListCreateAPIView):
    queryset = Gpssensor.objects.all()
    serializer_class = GpssensorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class GpssensorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gpssensor.objects.all()
    serializer_class = GpssensorSerializer


class GpsdataList(generics.ListCreateAPIView):
    queryset = Gpsdata.objects.all()
    serializer_class = GpsdataSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class GpsdataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gpsdata.objects.all()
    serializer_class = GpsdataSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ModelList(generics.ListCreateAPIView):
    def __init__(self, model):
        self.model = model
        super.__init__()

    def get_queryset(self):
        self.queryset = Model.objects.all()

    def get_serializer_class(self):
        self.serializer_class = OrderSerializer


class UploadFileViewSet(viewsets.ModelViewSet):
    queryset = UploadFile.objects.all()
    serializer_class = UploadFileSerializer
