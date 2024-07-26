from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, MessageViewSet, CreateRoomView, RoomListAPIView

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
        path('create/', CreateRoomView.as_view(), name='create_room'),
        path('list/', RoomListAPIView.as_view(), name='room_list_api'),
] + router.urls