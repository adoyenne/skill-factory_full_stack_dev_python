from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, MessageViewSet, CreateRoomView, RoomListAPIView, RoomDetailView

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('create/', CreateRoomView.as_view(), name='create_room'),
    path('api/', include(router.urls)),
    path('api/rooms/', RoomListAPIView.as_view(), name='room-list'),
    path('api/rooms/<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
] + router.urls