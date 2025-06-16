from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_product, name='add_product'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/like/', views.like_product, name='like_product'),
    path('product/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='products/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),]