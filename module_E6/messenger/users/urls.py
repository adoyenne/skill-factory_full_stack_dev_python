from django.urls import path
from .views import RegisterView, LoginView, profile_view, CustomLogoutView
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, profile_edit, user_list, send_message



router = DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='/home/'), name='logout'),
    path('profile/<int:pk>/', profile_view, name='profile'),  # URL для профиля
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('users/', user_list, name='user_list'),
    path('send-message/<int:recipient_id>/', send_message, name='send_message'),
] + router.urls


