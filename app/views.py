from django.shortcuts import render
import razorpay
from .models import Donation
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string



def home(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        amount=int(request.POST.get("amount"))*100
        # print(name,amount)
        client=razorpay.Client(auth=("rzp_test_o17EEDmxCPr9Dm","1J32FJkelVntz1Ei1kvgU0cF"))
        payment=client.order.create({"amount":amount,"currency":"INR","payment_capture":'1'})
        print(payment)
        donation=Donation(name=name,amount=amount,email=email,order_id=payment['id'])
        donation.save()
        return render(request,"index.html",{"payment":payment})

    return render(request,"index.html")



@csrf_exempt
def success(request):
    if request.method=="POST":
        a=request.POST
        order_id=''
        for key,val in a.items():
            if key=="razorpay_order_id":
                order_id=val
                break
        # print(order_id)
        user=Donation.objects.filter(order_id=order_id).first()
        user.paid=True
        user.save()


        msg_plain=render_to_string('email.txt')
        msg_html=render_to_string("email.html")

        send_mail("Your Donation Has been Received",msg_plain,settings.EMAIL_HOST_USER,
        ['user.email'],html_message=msg_html
        )


    return render(request,"success.html")