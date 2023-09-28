from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from robots.models import Robot
from orders.models import WaitingOrder


@receiver(post_save, sender=Robot)
def check_waiting_orders(sender, instance, created, **kwargs):
    
    if created:
        
        waiting_orders = WaitingOrder.objects.filter(
            robot_model=instance.model,
            robot_version=instance.version,
            quantity__lte=Robot.objects.filter(model=instance.model, version=instance.version).count()
        )
        for waiting_order in waiting_orders:
            email_message = f"Добрый день!\nНедавно вы интересовались нашим роботом модели {waiting_order.robot_model}, версии {waiting_order.robot_version}.\nЭтот робот теперь в наличии. Если вам подходит этот вариант - пожалуйста, свяжитесь с нами"
            send_mail(
                'Robot in stock',
                email_message,
                "from_admin@example.com",
                [waiting_order.customer.email],
                fail_silently=False,
            )
            waiting_order.delete()