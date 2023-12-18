from django.urls import path
from . import views

urlpatterns = [
    path('view_cart',views.view_cart, name='view_cart'),
    path('addtocart', views.add_to_cart, name='addtocart'),
    path('remove_cart_item/<int:cart_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('update_cart', views.update_cart, name='update_cart'),
    path('remove_coupon/<int:cart_id>/',views.remove_coupon, name='remove_coupon'),
    path('checkout', views.check_out, name='checkout'),
    path('check_wallet_balance', views.check_wallet_balance, name='check_wallet_balance'),
    path('place_order', views.place_order, name='place_order'),

    path('order_confirmation', views.order_confirmation, name='order_confirmation'),
    # path('update_cart', views.update_cart, name='update_cart'),
]
