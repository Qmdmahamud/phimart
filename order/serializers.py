from rest_framework import serializers
from order.models import Cart,CartItem,Order,OrderItem
from product.serializers import ProductSerializer
from product.models import Product
from order.services import OrderService


class EmptySerializer(serializers.Serializer):
    pass
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','name','price']


class CartItemSerializer(serializers.ModelSerializer):
    # product=ProductSerializer()
    product=SimpleProductSerializer()
    total_price=serializers.SerializerMethodField(method_name='get_total_price')
    # product_price=serializers.SerializerMethodField(method_name='get_product_price')
    class Meta:
        model=CartItem
        fields=['id','product','quantity','product','total_price']

    # def get_product_price(self,cart_item):
    #     return cart_item.product.price

    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity*cart_item.product.price
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id=serializers.IntegerField()
    class Meta:
        model=CartItem
        fields=['id','product_id','quantity']

    def save(self,**kwargs):
        cart_id=self.context['cart_id']
        product_id=self.validated_data['product_id']
        quantity=self.validated_data['quantity']

        try:
            cart_item=CartItem.objects.get(cart_id=cart_id,product_id=product_id)
            cart_item.quantity+=quantity
            self.instance=cart_item.save()
        except CartItem.DoesNotExist:
           self.instance= CartItem.objects.create(cart_id=cart_id,**self.validated_data)

        return self.instance
    def validate_product_id(self,value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(f"Product with id {value} does not exists")
        return value
class CartSerializer(serializers.ModelSerializer):
    items=CartItemSerializer(many=True,read_only=True)
    class Meta:
        model=Cart
        fields=['id','user','items']
        read_only_fields=['user']

    def get_total_price(self,cart:Cart):
        list=sum([item.product.price* item.quantity for item in cart.items.all()])
        print("list",list)
        return list
    
class CreateOrderSerializer(serializers.Serializer):
    cart_id= serializers.UUIDField()

    def validate_cart_id(self,cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart found with this id')
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart is empty')
        return cart_id

    def create(self,validated_data):
        user_id=self.context['user_id']
        cart_id= validated_data['cart_id']

        # cart=Cart.objects.get(pk=cart_id)
        # cart_items=cart.items.select_releted('product').all()

        # total_price=sum([item.product.price*item.quantity for item in cart_items])
        # order=Order.objects.create(user_id=user_id,total_price=total_price)
        
        # order_items=[
        #     OrderItem(
        #         order=order,
        #         product=item.product,
        #         price=item.product.price,
        #         qunatity=item.quantity,
        #         total_price=item.product.price* item.quantity
        #     )
        #     for item in cart_items

        # ]
        # OrderItem.objects.bulk_create(order_items)
        # cart.delete()
        # # print(user_id)
        # # print(cart_id)
        # return order
    def create(self,validated_data):
        user_id=self.context['user_id']
        cart_id=validated_data['cart_id']

        try:
            order=OrderService.create_order(user_id=user_id,cart_id=cart_id)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
    def to_representation(self, instance):
        return OrderSerializer(instance).data
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        fields=['quantity']
class OrderItemSerializer(serializers.ModelSerializer):
    product=SimpleProductSerializer()
    class Meta:
        model=OrderItem
        fields=['id','product','price','quantity','total_price']

class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['status']
    
    # def update(self,instance,validated_data):
    #     user=self.context['user']
    #     new_status=validated_data['status']

    #     if new_status==Order.CANCELED:
    #         return OrderSerializer.cancel_order(order=instance,user=user)
        
    #     # admin kina
    #     if not user.is_staff:
    #         raise serializers.ValidationError(
    #             {'detail': 'You are not allowed to update this order'}
    #         )
    #     # instance.status = new_status
    #     # instance.save()
    #     # return instance
    #     return super().update(instance,validated_data)

class OrderSerializer(serializers.ModelSerializer):
    items=OrderItemSerializer(many=True)
    class Meta:
        model=Order
        fields=['id','user','status','total_price','created_at','items']