from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from .views import register

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='book_list'), name='logout'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/new/', views.book_create, name='book_new'),
    path('book/<int:pk>/edit/', views.book_update, name='book_edit'),
    path('book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('register/', views.register, name='register'),
]