from django.urls import path
from . import views

urlpatterns = [
    path("",views.first,name="index"),
    path("contact",views.contact,name="contact"),
    path("aboutus",views.about,name="about"),
    path("signup/",views.signup,name="signup"),
    path("login/",views.login,name="login"),
    path("logout/",views.logout_user,name="logout"),
    path("products/",views.products,name="products"),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('my_cart/',views.my_cart,name="my_cart"),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('products_check_out/',views.products_check_out,name="products_check_out"),
    path('payment/',views.payment,name="payment"),
    path('thankyou/',views.thankyou,name="thankyou"),
    path('update_payment/',views.update_payment,name="update_payment"),
    path('my_orders',views.my_orders,name="my_orders"),
    path('activate/<uidb64>/<token>',views.activate_account,name='activate'),
]

