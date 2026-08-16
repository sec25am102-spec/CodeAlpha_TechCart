from django.contrib import admin
from django.urls import path
from store.views import (
    home,
    product_detail,
    add_to_cart,
    cart,
    increase_quantity,
    decrease_quantity,
    checkout,
    register,
    login_view,
    logout_view,
    place_order,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),

    path(
        'product/<int:product_id>/',
        product_detail,
        name='product_detail'
    ),

    path(
        'add-to-cart/<int:product_id>/',
        add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/',
        cart,
        name='cart'
    ),

    path(
        'cart/increase/<int:product_id>/',
        increase_quantity,
        name='increase_quantity'
    ),

    path(
        'cart/decrease/<int:product_id>/',
        decrease_quantity,
        name='decrease_quantity'
    ),

    path(
        'checkout/',
        checkout,
        name='checkout'
    ),

    path(
        'place-order/',
        place_order,
        name='place_order'
    ),

    path(
        'register/',
        register,
        name='register'
    ),

    path(
        'login/',
        login_view,
        name='login'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),
]