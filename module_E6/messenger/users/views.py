from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import login as django_login
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from .models import UserProfile
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserChangeForm, UserProfileForm
from django.contrib.auth import login
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm


User = get_user_model()

from .models import CustomUser

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            refresh = RefreshToken.for_user(user)

            # Автоматически вход пользователя после регистрации
            login(request, user)

            # Возвращаем токены как часть ответа
            response = redirect('home')  # перенаправляем на главную страницу после успешной регистрации
            response.set_cookie('access', str(refresh.access_token))
            response.set_cookie('refresh', str(refresh))
            return response

        return render(request, 'registration/register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        print('POST method called')  # Отладка
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            django_login(request, user)
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)

            # Debug print statements
            print('Access token:', access_token)
            print('Refresh token:', refresh_token)

            # Временно возвращаем простой ответ вместо перенаправления
            response = HttpResponse(f'Logged in. Access token: {access_token}, Refresh token: {refresh_token}')
            response.set_cookie('access_token', str(access_token), httponly=True)
            response.set_cookie('refresh_token', str(refresh_token), httponly=True)
            return response
        else:
            print('Form is not valid:', form.errors)
        return render(request, 'registration/login.html', {'form': form})


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Отладочная информация
        print(f"Request user: {request.user}")
        print(f"Request headers: {request.headers}")

        # Завершение сессии пользователя
        django_logout(request)

        # Удаление токенов из cookies, если они есть
        response = Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        # Получение и удаление refresh_token
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Если используете Blacklist
            except Exception as e:
                print(f"Error blacklisting token: {e}")

        return response

class CustomLogoutView(DjangoLogoutView):
    next_page = reverse_lazy('home')  # Переадресация на страницу home после выхода


@login_required
def profile_view(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'profile.html', {'user': user})


@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            # Перенаправление на страницу профиля текущего пользователя
            return redirect('profile', pk=request.user.pk)
    else:
        user_form = CustomUserChangeForm(instance=request.user)

    return render(request, 'registration/profile_edit.html', {'user_form': user_form})

def user_list(request):
    users = User.objects.exclude(id=request.user.id)  # Исключаем текущего пользователя
    return render(request, 'user_list.html', {'users': users})

@login_required
def send_message(request, recipient_id):
    recipient = get_object_or_404(CustomUser, id=recipient_id)
    return render(request, 'send_message.html', {'recipient': recipient})