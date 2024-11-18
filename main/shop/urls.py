from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import *
from django.urls import path

urlpatterns = [
    path('', ProductListView.as_view({'get': 'list', 'post': 'create'}), name='product_list'),
    path('<int:pk>', ProductDetailView.as_view({'get': 'retrieve',
                                                'put': 'update', 'delete': 'destroy'}), name='product_detail'),

    path('users/', ProfileListView.as_view({'get': 'list', 'post': 'create'}), name='users_list'),
    path('users/<int:pk>', ProfileDetailView.as_view({'get': 'retrieve',
                                                      'put': 'update', 'delete': 'destroy'}), name='users_detail'),

    path('category/', CategoryListView.as_view({'get': 'list', 'post': 'create'}), name='category_list'),
    path('category/<int:pk>', CategoryDetailView.as_view({'get': 'retrieve',
                                                         'put': 'update', 'delete': 'destroy'}), name='category_detail'),

    path('rating/', CategoryListView.as_view({'get': 'list', 'post': 'create'}), name='category_list'),
    path('rating/<int:pk>', CategoryDetailView.as_view({'get': 'retrieve',
                                                       'put': 'update', 'delete': 'destroy'}), name='review_detail'),
    path('review/', CategoryListView.as_view({'get': 'list', 'post': 'create'}), name='category_list'),
    path('review/<int:pk>', CategoryDetailView.as_view({'get': 'retrieve',
                                                       'put': 'update', 'delete': 'destroy'}), name='review_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('cart/', CartView.as_view({'get': 'retrieve'}), name='cart'),
    path('cart-add/', CartItemView.as_view({'post': 'create','get': 'list' }), name='cart_add'),
    path('cart-add/<int:pk>/', CartItemView.as_view({'put': 'update', 'delete': 'destroy'}), name='cart_add'),
]
