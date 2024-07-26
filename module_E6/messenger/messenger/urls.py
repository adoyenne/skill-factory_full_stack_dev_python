"""
URL configuration for messenger project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from chats.views import RoomListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Подключение URL-ов для пользователей
    path('api/rooms/', include('chats.urls')),  # API для комнат
    path('chat/', include('chats.urls')),  # URL для чата
    path('home/', TemplateView.as_view(template_name='index.html'), name='home'),
    path('', RedirectView.as_view(url='/home/', permanent=True)),  # Перенаправление с корня на /home/
    path('rooms/', RoomListView.as_view(), name='room_list'),  # Шаблон для списка комнат
    path('', include('django.contrib.auth.urls')),  # URL для аутентификации
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обслуживание статических файлов во время разработки
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])