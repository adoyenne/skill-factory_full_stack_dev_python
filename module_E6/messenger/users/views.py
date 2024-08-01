from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, get_user_model, login as django_login, logout as django_logout
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
from django.views.decorators.csrf import csrf_exempt


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
        else:
            errors = form.errors.as_json()
            return JsonResponse({'error': 'Invalid form data', 'details': errors}, status=400)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(f"Login attempt with username: {username}")
        user = authenticate(username=username, password=password)
        if user is not None:
            django_login(request, user)
            print("User authenticated successfully.")
            refresh = RefreshToken.for_user(user)
            response_data = {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
            return Response(response_data)
        print("Authentication failed.")
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
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