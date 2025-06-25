from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from django.urls import reverse
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from .forms import SignupForm
from users.models import User

class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        authenticated = authenticate(email=email, password=password)
        if authenticated is None:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
        else:
            login(request, authenticated)
            return redirect(reverse('home'))

class LoginAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'id': user.id,
            'nome': user.first_name,
            'email': user.email,
            'tipo': user.user_type,
            'foto': request.build_absolute_uri(user.photo.url) if user.photo else None,
            'token': token.key
        }, status=status.HTTP_200_OK)

class SignupView(View):
    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                password=request.POST.get('password'),
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                user_type=form.cleaned_data['user_type'],
                photo= request.FILES.get('photo', None)
            )
            if user is None:
                context = {
                    'form': form,
                    'error': 'Email already exists'
                }
                return render(request, 'signup.html', context)
            else:
                login(request, user)
                return redirect(reverse('home'))
        else:
            return render(request, 'signup.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        from django.contrib.auth import logout
        logout(request)
        return redirect(reverse('home'))