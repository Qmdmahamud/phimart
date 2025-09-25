from django.urls import path
from product import views


urlpatterns = [
    # path('',views.view_product,name='product-list'),
    path('',views.ViewProduct.as_view(),name='product-list'),
    # path('products/',views.view_product,name="product_list"),
    # path('<int:id>/',views.view_specific_product,name="product_list"),
    # path('<int:id>/',views.ViewSpecificProduct.as_view(),name="product_list"),
    path('<int:id>/',views.ProductDetails.as_view(),name="product_list"),
    # path('<int:pk>/',views.view_specific_category,name="product_list"),
    # path('categories/',views.view_categories,name='category-list'),
]
