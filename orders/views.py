import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Order, WaitingOrder
from customers.models import Customer
from robots.models import Robot

@csrf_exempt
def make_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        robot_serial = data['robot_serial']
        quantity = int(data['quantity'])
        custom_email = data['email']

        robot_summary = Robot.objects.filter(serial=robot_serial).count()
        
        if not robot_summary or quantity > robot_summary:
            customer, created = Customer.objects.get_or_create(email=custom_email)
            WaitingOrder.objects.create(
                customer=customer,
                robot_model=Robot.objects.filter(serial=robot_serial).first().model,
                robot_version=Robot.objects.filter(serial=robot_serial).first().version,
                quantity=quantity
            )
            message = "Пока заказ оформить не сможем, но вы добавлены в список ожидания."
        else:
            customer_email = custom_email
            customer, created = Customer.objects.get_or_create(email=customer_email)
            Order.objects.create(customer=customer, robot_serial=robot_serial)
            message = "Заказ успешно оформлен."

        return JsonResponse({'message': message})

    return JsonResponse({'error': 'Method not allowed'}, status=405)