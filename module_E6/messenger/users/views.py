from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, login as django_login, logout as django_logout
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.http import HttpResponseBadRequest


from .models import CustomUser
from .serializers import CustomUserSerializer
from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()

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
            django_login(request, user)
            response_data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            return JsonResponse(response_data)
        return JsonResponse({'error': 'Invalid form data'}, status=400)

class LoginView(APIView):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            django_login(request, user)
            access_token = AccessToken.for_user(user)
            refresh_token = RefreshToken.for_user(user)
            response_data = {
                'access': str(access_token),
                'refresh': str(refresh_token)
            }
            return JsonResponse(response_data)
        else:
            # Возвращаем ошибку в формате JSON
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        django_logout(request)
        refresh_token = request.data.get('refresh')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Если используем Blacklist
            except Exception as e:
                print(f"Error blacklisting token: {e}")
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

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
            return redirect('profile', pk=request.user.pk)
    else:
        user_form = CustomUserChangeForm(instance=request.user)
    return render(request, 'registration/profile_edit.html', {'user_form': user_form})

@login_required
def send_message(request, recipient_id):
    recipient = get_object_or_404(CustomUser, id=recipient_id)
    return render(request, 'send_message.html', {'recipient': recipient})

def user_list(request):
    users = User.objects.exclude(id=request.user.id)  # Исключаем текущего пользователя
    return render(request, 'user_list.html', {'users': users})