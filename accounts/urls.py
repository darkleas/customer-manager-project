from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
urlpatterns = [
    path("",views.home,name='dashboard'),
    path("products/",views.products,name='products'),
    path("create_order/",views.order_create,name='create_order'),
    path("update_order/<str:pv>/",views.order_update,name='update_order'),
    path("delete_order/<str:pv>/",views.delete_order,name='delete_order'),

    path("create_product/",views.product_create,name='create_product'),
    path("update_product/<str:pv>/",views.product_update,name='update_product'),
    path("delete_product/<str:pv>/",views.delete_product,name='delete_product'),

    path("orders/",views.orders,name='orders'),
    path("customer/<str:pv>/",views.customer,name='customer'),
    path("account/",views.accountPage,name="accountPage"),
    path("user/",views.userPage,name="userpage"),
    path("register/",views.register,name='register'),
    path("login/",views.Login,name='login'),
    path("logout/",views.Logout,name='logout'),

    path("reset_password/",
    auth_views.PasswordResetView.as_view(template_name='accounts\password_reset.html')
    ,name='reset_password'),
    path("reset_password_sent/",views.passwordresetsent,name='password_reset_done'),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name='accounts\email_reset.html'),name='password_reset_confirm'),
    path("reset_password_complete/",views.passwordresetcomplete,name='password_reset_complete'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

