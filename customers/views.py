import json

from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Director

@csrf_exempt
def register_director(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = User.objects.create_user(username=username, password=password)
        director = Director(user=user, is_director=True)
        director.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Registration successful'}, status=201)
   
    return JsonResponse({'error': 'Invalid registration data'}, status=400)

@csrf_exempt
def login_director(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None and user.director.is_director:
            login(request, user)
            return JsonResponse({'message': 'Login successful'})

    return JsonResponse({'error': 'Login failed'}, status=401)

@csrf_exempt
def logout_director(request):
    if request.method == 'POST':
    
        logout(request)
        return JsonResponse({'message': 'Logout successful'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)
