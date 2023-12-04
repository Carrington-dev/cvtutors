from django.urls import  path
from cart import views as cart_views

urlpatterns = [
    path('', cart_views.cart, name="cart"),
    path('add_cart/<int:product_id>/', cart_views.add_cart, name="add_cart"),
    path('add_cart_course/<int:course_id>/', cart_views.add_cart_course, name="add_cart_course"),
    path('remove_cart/<int:cart_item_id>/', cart_views.remove_cart, name="remove_cart"),
    path('increase-item/<int:cart_item_id>/', cart_views.increase_cart, name="increase_cart"),
    path('delete_cart/<int:cart_item_id>/', cart_views.delete_cart_item, name="delete_cart_item"),
   
    # path('update-cart-item/', cart_views.updateItem, name='update_item'),
]