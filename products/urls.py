from .views import MyProductView, MyProductDetailView, CategoryView, ProductDetailView, CompanyProductsListView, ProductsListSearchView
from django.urls import path

urlpatterns = [
    path('myproducts/', MyProductView.as_view(), name="product_view"),
    path('myproducts/<int:pk>', MyProductDetailView.as_view(), name="product_detail_view"),
    path('categories/', CategoryView.as_view(), name="category_view"),
    path('<int:pk>', ProductDetailView.as_view(), name="product_view"),
    path('', CompanyProductsListView.as_view(), name="product_view"),
    path('public/', ProductsListSearchView.as_view(), name="public_product_view"),
]
