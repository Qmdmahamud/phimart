from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product,Category,Review,ProductImage
from rest_framework import status
from product.serializers import ProductSerializer,CategorySerializer,ReviewSerializer,ProductImagesSerializer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
# from rest_framework.pagination import PageNumberPagination
from product.paginations import DefaultPagination
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from api.permissions import IsAdminReadOnly
from product.permissions import IsReviewAuthorOrReadonly
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class ProductViewSet(ModelViewSet):
    """
    API endpoint for managing products in the e-commerce store
    -Allows authenticated admin to create,updaate, and delete products
    -Allows users to browse and filter product
    -Support searching by name,description, and category
    -Support ordering by price and updated_at
    """
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    filter_backends=[DjangoFilterBackend,SearchFilter,OrderingFilter] #Search korar jonno use kora hocce
    Ordering_fields=['price','updated_at']
    # filter_fields=['category_id','price']
    filterset_class=ProductFilter
    # pagination_class=PageNumberPagination
    pagination_class=DefaultPagination
    search_fields=['name','description']
    # permission_classes=[IsAdminUser]
    permission_classes=[IsAdminReadOnly]

    @swagger_auto_schema(
            operation_summary='Retrive a list of products'
    )
    def list(self,request,*args, **kwargs):
        """Retrive all the create product"""
        return super().list(request,*args, **kwargs)
    
    @swagger_auto_schema(
            operation_summary="Create a product by admin",
            operation_description="This allow an admin to create a product",
            request_body=ProductSerializer,
            responses={
                201:ProductSerializer,
                400:"Bad Request"
            }
    )
    def create(self,request,*args,**kwargs):
        """Only authenticated admin can create product"""
        return super().create(request,*args, **kwargs)

    # def get_permissions(self):
    #     if self.request.method=='GET':
    #         return [AllowAny()]
    #     return [IsAdminUser()]

    # def get_queryset(self):
    #     queryset=Product.objects.all()
    #     category_id=self.request.query_params.get('category_id')

    #     if category_id is not None:
    #         queryset=Product.objects.filter(category_id=category_id)
    #     return queryset

    # def destroy(self,request,pk=None,*args, **kwargs):
    #     # product=get_object_or_404(Product,pk=id)
    #     product=self.get_object()
    #     if product.stock>10:
    #         return Response({'message':"Product with stock more than 10 could not be deleted"})
    #     # copy_of_product=product
    #     self.perform_destroy(product)
    #     product.delete()
    #     # serializer=ProductSerializer(copy_of_product)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

class ProductImageViewSet(ModelViewSet):
    serializer_class=ProductImagesSerializer
    permission_classes=[IsAdminReadOnly]
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs.get('product_pk'))

    def perform_create(self,serializer):
        serializer.save(product_id=self.kwargs.get('product_pk'))

class CategoryViewSet(ModelViewSet):
    permission_classes=[IsAdminReadOnly]
    queryset=Category.objects.annotate(
        product_count=Count('products')
    ).all()
    serializer_class=CategorySerializer
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes=[IsReviewAuthorOrReadonly]

    def get_queryset(self):
        product_id = self.kwargs.get('product_pk')  # nested router থেকে product_pk আসবে
        return Review.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        # serializer এ context পাঠানো হচ্ছে
        return {"product_id": self.kwargs.get("product_pk"), "request": self.request}
    def get_serializer_context(self):
        return {'product_id':self.kwargs.get('product_pk')}

# class ReviewViewSet(viewsets.ModelViewSet):
#     # queryset=Review.objects.all()
#     serializer_class=ReviewSerializer
#     def perform_create(self,serializer):
#         serializer.save(user=self.request.user)
#     def get_queryset(self):
#         return Review.objects.filter(product_id=self.kwargs['product_pk'])

#     def get_serializer_context(self):
#         return {'product_id':self.kwargs['product_pk']}

# @api_view(['GET','POST'])
# def view_product(request):
#     if request.method=='GET':
#         products=Product.objects.select_related('category').all()
#         serializer=ProductSerializer(products,many=True,context={'request':request})
#         return Response(serializer.data)
#     if request.method=='POST':
#         serializer=ProductSerializer(data=request.data,context={'request':request}) #deserializer
#         if serializer.is_valid():
#             print(serializer.validated_data)
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ViewProduct(APIView):
    def get(self,request):
        products=Product.objects.select_related('category').all()
        serializer=ProductSerializer(products,many=True,context={'request':request})
        return Response(serializer.data)
    def post(self,request):
        serializer=ProductSerializer(data=request.data,context={'request':request}) #deserializer
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

# class ProductList(ListCreateAPIView):
#     queryset=Product.objects.select_related('category').all()
#     serializer_class=ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.select_related('category').all()
    # def get_serializer_class(self):
    #     return ProductSerializer
    # def get_serializer_context(self):
    #     return {'request':self.request}
class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='id'

    # def delete(self,request,id):
    #     product=get_object_or_404(Product,pk=id)
    #     if product.stock>10:
    #         return Response({'message':"Product with stock more than 10 could not be deleted"})
    #     # copy_of_product=product
    #     product.delete()
    #     # serializer=ProductSerializer(copy_of_product)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
                    
# @api_view(['GET','PUT','DELETE'])
# def view_specific_product(request,id):
#     if request.method=='GET':
#         # try:
#         # product=Product.objects.get(pk=id)
#         product=get_object_or_404(Product,pk=id)
#         # product_dict={'id':product.id,'name':product.name,'price':product.price}
#         serializer=ProductSerializer(product)
#         # return Response({"messaage":"Okay"})
#         return Response(serializer.data)
#         # except Product.DoesNotExist:
#         #     return Response({'message':'id does not have here'},status=status.HTTP_404_NOT_FOUND)
#     if request.method=='PUT':
#         product=get_object_or_404(Product,pk=id)
#         serializer=ProductSerializer(product,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     if request.method=='DELETE':
#         product=get_object_or_404(Product,pk=id)
#         copy_of_product=product
#         product.delete()
#         serializer=ProductSerializer(copy_of_product)
#         return Response(status=status.HTTP_204_NO_CONTENT)

# class ViewSpecificProduct(APIView):
#     def get(self,request,id):
#         # try:
#         # product=Product.objects.get(pk=id)
#         product=get_object_or_404(Product,pk=id)
#         # product_dict={'id':product.id,'name':product.name,'price':product.price}
#         serializer=ProductSerializer(product)
#         # return Response({"messaage":"Okay"})
#         return Response(serializer.data)
#         # except Product.DoesNotExist:
#         #     return Response({'message':'id does not have here'},status=status.HTTP_404_NOT_FOUND)
#     def put(self,request,id):
#         product=get_object_or_404(Product,pk=id)
#         serializer=ProductSerializer(product,data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     def delete(self,request,id):
#         product=get_object_or_404(Product,pk=id)
#         copy_of_product=product
#         product.delete()
#         serializer=ProductSerializer(copy_of_product)
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

# @api_view()
# def view_categories(request):
#     categories=Category.objects.annotate(product_count=Count('products')).all()
#     serializer=CategorySerializer(categories,many=True)
#     return Response(serializer.data)
# class CategoryDetails(RetrieveUpdateDestroyAPIView):
#     queryset=Category.objects.annotate(
#         product_count=Count('product')).all()
#     serializer_class=CategorySerializer
# class ViewCategory(APIView):
#     def get(self,request):
#         categories=Category.objects.annotate(product_count=Count('products')).all()
#         serializer=CategorySerializer(categories,many=True)
#         return Response(serializer.data)
#     def post(self,request):
#         seralizer=CategorySerializer(data=request.data)
#         seralizer.is_valid(raise_exception=True)
#         seralizer.save()
#         return Response(seralizer.data,status=status.HTTP_201_CREATED)
    
#     def put(self,reequest,id):
#         categories=Category.objects.annotate(product_count=Count('products')).all()
#         serialalizer=CategorySerializer(categories,data=reequest.data)
#         serialalizer.is_valid(raise_exception=True)
#         serialalizer.save()
#         return Response(serialalizer.data)
#     def delete(self,request,id):
#         categories=Category.objects.annotate(product_count=Count('products')).all()
#         categories.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)



# @api_view()
# def view_specific_category(request,pk):
#     category=get_object_or_404(Category.objects.annotate(product_count=Count('products')).all())
#     serializer=CategorySerializer(category)
#     return Response(serializer.data)

# class ViewSpecificCategory(APIView):
#     def category(self,request,pk):
#         category=get_object_or_404(Category,pk=pk)
#         serializer=CategorySerializer(category)
#         return Response(serializer.data)

# from rest_framework import viewsets
# from .models import Review
# from .serializers import ReviewSerializer

# class ReviewViewSet(viewsets.ModelViewSet):
#     serializer_class = ReviewSerializer

#     def get_queryset(self):
#         product_id = self.kwargs.get("product_pk")  # Nested router থেকে product_pk আসে
#         return Review.objects.filter(product_id=product_id)
#     def perform_create(self, serializer):
#         # create করার সময় product এবং user attach করে দিচ্ছি
#         product_id = self.kwargs.get("product_pk")
#         serializer.save(
#             product_id=product_id,
#             user=self.request.user
#         )