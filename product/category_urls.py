from django.urls import path
from product import views


urlpatterns = [
    # path('products/',views.view_product,name="product_list"),
    # path('',views.view_product,name="product_list"),
    # path('categories/',views.view_categories,name='category-list'),
    path('',views.view_categories,name='category-list'),
    # path('<int:pk>/',views.view_specific_category,name='view_specific_category')
    # path('<int:pk>/',views.ViewSpecificCategory.as_view(),name='view_specific_category')
    path('<int:pk>/',views.CategoryDetails.as_view(),name='view_specific_category')
]
