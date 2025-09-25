from order.models import Cart,CartItem,OrderItem,Order
from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError


class OrderService:
    @staticmethod
    def create_order(user_id,cart_id):
        with transaction.atomic():
        
            cart=Cart.objects.get(pk=cart_id)
            cart_items=cart.items.select_releted('product').all()

            total_price=sum([item.product.price*item.quantity for item in cart_items])
            order=Order.objects.create(user_id=user_id,total_price=total_price)
            
            order_items=[
                OrderItem(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    qunatity=item.quantity,
                    total_price=item.product.price* item.quantity
                )
                for item in cart_items

            ]
            OrderItem.objects.bulk_create(order_items)
            cart.delete()
            # print(user_id)
            # print(cart_id)
            return order
        
        @staticmethod
        def cancel_order(order,user):
            if user.is_staff:
                order.status=order.CANCLED
                order.save()
                return order
            if order.user != user:
                raise PermissionDenied({'detail': "You can only cancel your own order"})
            if order.status==Order.DELIVERED:
                raise ValidationError({'detail': "You can not cancel an order"})