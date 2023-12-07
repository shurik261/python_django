from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShopIndexView,
    GroupsListView,
    ProductDetailsView,
    ProductListView,
    OrderListView,
    OrderDetailsView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    OrderExportView,
    ProductViewSet,
    OrderViewSet,

)

routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)
app_name = 'shopapp'
urlpatterns = [
    path('', ShopIndexView.as_view(), name='index'),
    path('api/', include(routers.urls)),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/create/', ProductCreateView.as_view(), name='create_products'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='products_details'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name='products_update'),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name='products_delete'),
    path('orders/', OrderListView.as_view(), name='orders_list'),
    path('orders/export/', OrderExportView.as_view(), name='orders_export'),
    path('orders/<int:pk>/', OrderDetailsView.as_view(), name='orders_details'),
    path('orders/create/', OrderCreateView.as_view(), name='orders_create'),
    path('orders/<int:pk>/update/', OrderUpdateView.as_view(), name='orders_update'),
    path('orders/<int:pk>/confirm-delete/', OrderDeleteView.as_view(), name='orders_delete'),
]