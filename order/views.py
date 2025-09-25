from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin,RetrieveModelMixin
from order.models import Cart,CartItem,Order,OrderItem
from order.serializers import CartSerializer
from order.serializers import EmptySerializer,UpdateOrderSerializer,CreateOrderSerializer,UpdateCartItemSerializer,AddCartItemSerializer,CartItemSerializer,CartSerializer,OrderSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.decorators import action
from order.services import OrderService
from rest_framework.response import Response
# Create your views here.
class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset=Cart.objects.all()
    serializer_class=CartSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user)

class CartItemViewSet(ModelViewSet):
    # queryset=CartItem.objects.all()
    # serializer_class=CartItemSerializer
    http_method_names=['get','post','patch','delete']

    def get_serializer_class(self):
        if self.request.method=='POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH':
            return UpdateCartItemSerializer

        return CartItemSerializer
    def get_serializer_context(self):
        context=super().get_serializer_context()
        if getattr(self,'swagger_fake_view',False):
            return context
        return {'cart_id':self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs.get('cart_pk'))
    

class OrderViewSet(ModelViewSet):
    # queryset=Order.objects.all()
    # serializer_class=OrderSerializer
    # permission_classes=[IsAuthenticated]
    http_method_names=['get','post','delete','patch','head','options']
    # permission_classes=[IsAuthenticated]
    @action(detail=True,methods=['patch'])
    def update_status(self,request,pk=None):
        order=self.get_object()
        serializer=UpdateOrderSerializer(
            order,data=request.data,partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status':f"Order status updatae to {request.data['status']}"})
    @action(detail=True,methods=['post'])
    def cancel(self,request,pk=None):
        order=self.get_object()
        OrderService.cancel_order(order=order,user=request.user)
        return Response({'status':'Order canceled'})
    def get_permissions(self):
        # if self.request.method in ['PATCH','DELETE']:
        if self.action in ['update_status','destroy']:
            return [IsAdminUser]
        return [IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.action =='cancel':
            return EmptySerializer
        if self.action =='create':
            return CreateOrderSerializer
        elif self.action=='partial_update':
            return UpdateOrderSerializer
        return OrderSerializer
    def get_serializer_context(self):
        if getattr(self,'swagger_fake_view',False):
            return super().get_serializer_context()
        return {'user_id':self.request.user.id,'user':self.request.user}

    def get_queryset(self):
        if getattr(self,'swagger_fake_view',False):
            return Order.objects.none()
        if self.request.user.is_staff():
            return Order.objects.prefetch_related('items__product').all()
        elif self.request.method=='PATCH':
            return UpdateOrderSerializer
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)