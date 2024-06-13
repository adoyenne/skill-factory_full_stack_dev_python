from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home_redirect, name='home'),  # Перенаправляем на профиль, если пользователь аутентифицирован
    path('post/list/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/response/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/delete_confirm/', views.post_delete_confirm, name='post_delete_confirm'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('response/<int:pk>/edit/', views.edit_comment, name='edit_comment'),  # Добавляем URL для редактирования комментариев
    path('response/<int:pk>/delete/', views.delete_comment, name='delete_comment'),  # Добавляем URL для удаления комментариев
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='post_list'), name='account_logout'),
    path('comment/<int:pk>/accept/', views.accept_response, name='accept_response'),
    path('responses/manage/', views.manage_responses, name='manage_responses'),
    path('comment/<int:pk>/delete/confirm/', views.delete_comment_confirm, name='delete_comment_confirm'),



]
