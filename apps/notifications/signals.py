from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.orders.models import Order
from apps.payments.models import Payment
from .models import Notification
from .utils import send_notification_email



@receiver(post_save, sender=Order)
def order_status_notification(sender, instance, created, **kwargs):

    if created:
        return

    Notification.objects.create(
        user=instance.user,
        title="Order Status",
        message=f"Your order {instance.order_number} is {instance.status}."
    )

    send_notification_email(
        "Order Status Updated",
        f"Your order {instance.order_number} is {instance.status}.",
        instance.user.email
    )



@receiver(post_save, sender=Payment)
def payment_notification(sender, instance, created, **kwargs):

    if created:
        return

    if instance.status == "Success":

        Notification.objects.create(
            user=instance.order.user,
            title="Payment Success",
            message=f"Payment received for {instance.order.order_number}."
        )

        send_notification_email(
            "Payment Successful",
            f"Payment received for order {instance.order.order_number}.",
            instance.order.user.email
        )

    elif instance.status == "Failed":

        Notification.objects.create(
            user=instance.order.user,
            title="Payment Failed",
            message=f"Payment failed for {instance.order.order_number}."
        )

        send_notification_email(
            "Payment Failed",
            f"Payment failed for order {instance.order.order_number}.",
            instance.order.user.email
        )

    elif instance.status == "Refunded":

        Notification.objects.create(
            user=instance.order.user,
            title="Refund Completed",
            message=f"Refund completed for {instance.order.order_number}."
        )

        send_notification_email(
            "Refund Completed",
            f"Refund completed for order {instance.order.order_number}.",
            instance.order.user.email
        )