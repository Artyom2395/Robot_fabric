import openpyxl
import json

from django.db.models import Count

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Robot

from robots.decorators import admin_required

@admin_required
@csrf_exempt
def create_robot(request):
    if request.method == 'POST':
        try:
            # Получение данных из запроса
            data = json.loads(request.body)
            model = data['model']
            version = data['version']
            created = data['created']
            
            if Robot.objects.filter(model=model, version=version, created=created).exists():
                return JsonResponse({'error': 'Robot with specified parameters already exists'}, status=400)
            
            serial = f"{model}-{version}"
            # Создание робота
            robot = Robot(serial=serial, model=model, version=version, created=created)
            robot.save()
            
            return JsonResponse({'success': 'Robot created'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@admin_required
def list_robots(request):
   
    robot_counts = Robot.objects.values('model').annotate(model_count=Count('id'))

    robots = Robot.objects.all()
    robot_data = []

    for robot in robots:
        robot_data.append({
            'serial': robot.serial,
            'model': robot.model,
            'version': robot.version,
        })

    return JsonResponse({'robot_counts': list(robot_counts), 'robots': robot_data})