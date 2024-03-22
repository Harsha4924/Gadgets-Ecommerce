from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import User
import json
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from .utils import TokenGenerator,generate_token
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.views.decorators.csrf import  csrf_exempt





from . import users,emailer,allproducts,keys,Checksum,confirmation,utils
# Create your views here.



def first(request):
    return render(request,"ecommerceapp/index.html")

def contact(request):
    return render(request,"ecommerceapp/contact.html")

def about(request):
    return render(request,"ecommerceapp/about.html")

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        # password = request.POST['password']
        # hashed_password = pwd_context.hash(password)
        hashed_password = utils.hash_it(request.POST['password'])
        try:
            present = users.get_user(email)
            if present:
                return HttpResponse("Email Already Exists")
        except Exception as identifier:
            pass
        users.update_users(email,hashed_password)
        primary_key = users.get_details(email)
        print("orders",primary_key)

        email_subject = "Activate Your Account"
        message = render_to_string('ecommerceapp/activate.html',{
            'primary_key' : primary_key,
            'domain': '127.0.0.1:8000',
            'uid' : urlsafe_base64_encode(force_bytes(primary_key['id'])),
            'token' : generate_token.make_token(primary_key),
        })
        print(message)

        send_email = emailer.send_verify_email(message,email)
        if send_email:
            messages.success(request,f"Activate Your Account by clicking the link in your gmail")
            return redirect('/login')
        else:
            return HttpResponse("Error occured Try after sometime")
    return render(request,'ecommerceapp/signup.html')


def activate_account(request,uidb64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        print("uid",uid)
        user=users.get_user_id(uid)
        print(user)
    except Exception as identifier:
        user=None
    if user is not None and generate_token.check_token(user,token):
        
        users.make_status_active(uid)
        messages.info(request,"Account Activated Successfully")
        return redirect('/login')
    # return render(request,'activatefail.html')



logged_in = None

def login(request):
    global logged_in
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            check = users.get_user_details(email,password)
            print("main", check)
            if check:
                logged_in = True
                return HttpResponseRedirect(f'/products/?user_id={check}')
            else:
                return HttpResponse("Invalid Credentials")
        except Exception as identifier:
            pass
    return render(request,'ecommerceapp/login.html')

def logout_user(request):
    logout(request)
    return redirect('/login')

def products(request):

    # if not request.user.is_authenticated:
    #     return redirect('/login')
    
    user_id = request.GET.get('user_id')
    global logged_in
    get_products = allproducts.get_all_products()
    quantities = list(range(1, 11))
    return render(request,"ecommerceapp/products.html",{'check':logged_in,'products':get_products,'user_id':user_id,'quantities':quantities})

def add_to_cart(request):
    if request.method == "POST":
        print("boom")
        product_id = request.POST.get('product_id')
        user = request.POST.get('user')
        quantity = request.POST.get('quantity')
        add = allproducts.adding_to_cart(product_id,user,quantity)
        if add:
            print(product_id,user,quantity)
            return JsonResponse({'message': 'Item added to cart successfully'})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)

def my_cart(request):
    user_id = request.GET.get('user_id')
    cart_items = allproducts.my_cart_items(user_id)
    return render(request,'ecommerceapp/my_cart.html',{'user_id':user_id,'cart_items':cart_items})

def remove_from_cart(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        product_id = request.POST['product_id']
        remove = allproducts.remove_product(user_id,product_id)
        if remove:
            return JsonResponse({'message': 'Item removed from cart successfully'})
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


MERCHANT_KEY=keys.MK


def products_check_out(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        email = users.get_user_email(user_id)
        total_cart_items_str=request.POST['total_cart_items']
        print("check",total_cart_items_str)
        total_cart_items = json.loads(total_cart_items_str)
        print("boom",total_cart_items)
        user_address = request.POST['user_address']
        total_price = request.POST['total_price']
        order_id = allproducts.fetch_order_id(user_id,total_price)
        # if order_id:
        #     oid = str(order_id)+"tonworld"
        #     param_dict = {
        #         'MID':keys.MID,
        #         'ORDER_ID': oid,
        #         'TXN_AMOUNT': str(total_price),
        #         'CUST_ID': email[0],
        #         'INDUSTRY_TYPE_ID': 'Retail',
        #         'WEBSITE': 'WEBSTAGING',
        #         'CHANNEL_ID': 'WEB',
        #         'CALLBACK_URL': 'http://127.0.0.1:8000/handlerequest/',
        #     }
        #     # MERCHANT_KEY=keys.MK
        #     param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)

        if order_id:

            for item in total_cart_items:
                product_id = int(item.get('product_id'))
                product_name = item.get('product_name')
                quantity = int(item.get('quantity'))
                payment = False
                all_orders = allproducts.insert_all_orders(order_id,user_id,product_id,quantity,product_name,payment)
            return JsonResponse({'success': True, 'total_price': total_price,'order_id':order_id})
        else:
            # Return an error response if order_id is not retrieved
            return JsonResponse({'error': 'Failed to fetch order ID'}, status=500)
    # return JsonResponse({'error': 'Method not allowed'}, status=405)
    raise Http404("Method not allowed")


def update_payment(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        user_email = users.get_user_email(user_id)
        order_id = request.POST['order_id']
        updates = allproducts.update_user_payment(user_id,order_id)
        message = confirmation.message
        print(message)
        subject = confirmation.subject
        print(subject)

        if updates:
            send_verification = emailer.send_verify_email(message,user_email,subject)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Failed to fetch order ID'}, status=500)
    raise Http404("Method not allowed")
    

    

def payment(request):
    user_id = request.GET.get('user_id')
    return render(request,'ecommerceapp/payment.html',{'user_id':user_id})

def thankyou(request):
    user_id = request.GET.get('user_id')
    return render(request,'ecommerceapp/thankyou.html',{'user_id':user_id})


def my_orders(request):
    user_id = request.GET.get('user_id')
    items = allproducts.retrieve_my_orders(user_id)
    return render(request,"ecommerceapp/my_orders.html",{'user_id':user_id,'items':items})
        
# @csrf_exempt
# def handlerequest(request):
#     # paytm will send you post request here
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]

#     verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('order successful')
#             a=response_dict['ORDERID']
#             b=response_dict['TXNAMOUNT']
#             rid=a.replace("tonworld","")
           
#             print(rid)
#        
#         else:
#             print('order was not successful because' + response_dict['RESPMSG'])
#     return render(request, 'paymentstatus.html', {'response': response_dict})
        