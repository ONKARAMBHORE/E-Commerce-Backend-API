import hmac
import hashlib
from django.db.models.aggregates import Sum
from django.db.models.functions import TruncDate, TruncMonth
import razorpay

from django.conf import settings
from django.utils import timezone
from django.db import transaction

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from apps.orders.models import Order
from .models import Payment
from .serializers import PaymentSerializer

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

from django.core.mail import send_mail


from apps.notifications.models import Notification
from apps.notifications.utils import send_notification_email


client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))



# PAYMENT VIEWSET
class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.select_related("order", "order__user").order_by("-created_at")

# CASH ON DELIVERY

    @action(detail=False, methods=["post"])  # COD payment
    def cod(self, request):
        order = Order.objects.get(
            pk=request.data["order"]  # Get order
        )

        payment = Payment.objects.create(
            order=order,
            payment_method="COD",
            amount=order.total,
            status="Pending"
        )  # Create payment

        order.payment_method = "COD"      # Payment method
        order.payment_status = "Pending"  # Payment status
        order.save()                      # Save order

        return Response(
            PaymentSerializer(payment).data  # Return payment
        )


        #Create Razorpay Order
        
    @action(detail=False, methods=["post"])  # Razorpay order
    def razorpay_order(self, request):
        order = Order.objects.get(
            pk=request.data["order"]  # Get order
        )

        razor_order = client.order.create({
            "amount": int(order.total * 100),  # Amount in paise
            "currency": "INR",                 # Currency
            "payment_capture": 1               # Auto capture
        })

        payment = Payment.objects.create(
            order=order,
            payment_method="RAZORPAY",
            amount=order.total,
            razorpay_order_id=razor_order["id"]
        )  # Create payment

        return Response({
            "razorpay_order_id": razor_order["id"],  # Razorpay order
            "amount": razor_order["amount"],         # Amount
            "currency": "INR",                       # Currency
            "payment_id": payment.id                # Payment ID
        })    


        #Verify Payment


    @action(detail=False, methods=["post"])
    @transaction.atomic
    def verify(self, request):

        payment = Payment.objects.select_related("order").get(pk=request.data["payment"])

        params = {
            "razorpay_order_id": payment.razorpay_order_id,
            "razorpay_payment_id": request.data["razorpay_payment_id"],
            "razorpay_signature": request.data["razorpay_signature"]
        }

        try:
            client.utility.verify_payment_signature(params)
        except:
            raise ValidationError({"detail": "Invalid Signature"})

        payment.razorpay_payment_id = params["razorpay_payment_id"]
        payment.transaction_id = params["razorpay_payment_id"]
        payment.status = "Success"
        payment.paid_at = timezone.now()
        payment.save()

        # Create notification
        Notification.objects.create(
            user=request.user,
            title="Payment Successful",
            message=f"Payment received for Order {order.order_number}."
        )

    # Send email
        send_notification_email(
            "Payment Successful",
            f"Your payment for Order {order.order_number} was successful.",
            request.user.email
        )

        order = payment.order
        order.payment_status = "Paid"
        order.status = "Confirmed"
        order.save()


        # email receipt

        send_mail(
            "Payment Successful",
            f"Payment received.\nOrder: {order.order_number}\nAmount: ₹{payment.amount}",
            None,
            [request.user.email]
        )

        return Response(PaymentSerializer(payment).data)



    # payment failed 


    @action(detail=True, methods=["patch"])
    def failed(self, request, pk=None):

        payment = self.get_object()

        payment.status = "Failed"
        payment.save()

        payment.order.payment_status = "Failed"
        payment.order.save()

        return Response({"message": "Payment Failed"})

    # Retry Payment


    @action(detail=True, methods=["post"])
    def retry(self, request, pk=None):

        payment = self.get_object()

        if payment.status == "Success":
            raise ValidationError({"detail": "Already Paid"})

        razor_order = client.order.create({
            "amount": int(payment.amount * 100),
            "currency": "INR",
            "payment_capture": 1
        })

        payment.razorpay_order_id = razor_order["id"]
        payment.status = "Pending"
        payment.save()

        return Response({
            "payment": payment.id,
            "razorpay_order_id": razor_order["id"],
            "amount": razor_order["amount"]
        })



    # Transaction History

    @action(detail=False, methods=["get"])
    def history(self, request):

        payments = self.get_queryset().order_by("-created_at")
        serializer = PaymentSerializer(payments, many=True)

        return Response(serializer.data)






# refund apis

        # Refund API

    @action(detail=True, methods=["post"])  # Refund payment
    @transaction.atomic
    def refund(self, request, pk=None):
        payment = self.get_object()  # Get payment

        if payment.status != "Success":
            raise ValidationError({"detail": "Only successful payments can be refunded."})

        if payment.payment_method == "COD":
            raise ValidationError({"detail": "COD cannot be refunded online."})

        payment.status = "Refunded"  # Update status
        payment.save()

        order = payment.order  # Get order
        order.payment_status = "Refunded"
        order.status = "Cancelled"
        order.save()

        for item in order.items.select_related("product"):
            item.product.stock += item.quantity  # Restore stock
            item.product.save(update_fields=["stock"])

        return Response({"message": "Refund completed."})


    # Payment Summary

    @action(detail=False, methods=["get"])  # Summary API
    def summary(self, request):
        payments = self.get_queryset().filter(status="Success")
        total = sum(p.amount for p in payments)

        return Response({
            "total_transactions": payments.count(),
            "total_revenue": total
        })


    # Recent Payments

    @action(detail=False, methods=["get"])  # Recent payments
    def recent(self, request):
        payments = self.get_queryset()[:10]
        return Response(PaymentSerializer(payments, many=True).data)


    # Payment Details

    @action(detail=True, methods=["get"])  # Payment details
    def details(self, request, pk=None):
        payment = self.get_object()
        return Response(PaymentSerializer(payment).data)


    # Successful Payments

    @action(detail=False, methods=["get"])  # Success list
    def successful(self, request):
        payments = self.get_queryset().filter(status="Success")
        return Response(PaymentSerializer(payments, many=True).data)


    # Failed Payments

    @action(detail=False, methods=["get"])  # Failed list
    def failed_payments(self, request):
        payments = self.get_queryset().filter(status="Failed")
        return Response(PaymentSerializer(payments, many=True).data)


    # Pending Payments

    @action(detail=False, methods=["get"])  # Pending list
    def pending(self, request):
        payments = self.get_queryset().filter(status="Pending")
        return Response(PaymentSerializer(payments, many=True).data)


    # Daily Revenue

    @action(detail=False, methods=["get"])  # Daily report
    def daily_report(self, request):
        report = Payment.objects.filter(
            status="Success"
        ).annotate(
            day=TruncDate("created_at")
        ).values(
            "day"
        ).annotate(
            total=Sum("amount")
        ).order_by("-day")

        return Response(report)


    # Monthly Revenue

    @action(detail=False, methods=["get"])  # Monthly report
    def monthly_report(self, request):
        report = Payment.objects.filter(
            status="Success"
        ).annotate(
            month=TruncMonth("created_at")
        ).values(
            "month"
        ).annotate(
            total=Sum("amount")
        ).order_by("-month")

        return Response(report)


    # Payment Analytics

    @action(detail=False, methods=["get"])  # Analytics
    def analytics(self, request):
        qs = Payment.objects

        return Response({
            "total": qs.count(),
            "success": qs.filter(status="Success").count(),
            "failed": qs.filter(status="Failed").count(),
            "pending": qs.filter(status="Pending").count(),
            "refunded": qs.filter(status="Refunded").count()
        })




# Razorpay Webhook 



# -------------------------
# Razorpay Webhook
# -------------------------

@csrf_exempt
def webhook(request):

    payload = request.body
    signature = request.headers.get("X-Razorpay-Signature")

    try:
        client.utility.verify_webhook_signature(
            payload,
            signature,
            settings.RAZORPAY_WEBHOOK_SECRET
        )
    except:
        return HttpResponse(status=400)

    event = json.loads(payload)

    if event["event"] == "payment.captured":

        payment_id = event["payload"]["payment"]["entity"]["id"]

        Payment.objects.filter(
            razorpay_payment_id=payment_id
        ).update(
            status="Success"
        )

    return HttpResponse(status=200)