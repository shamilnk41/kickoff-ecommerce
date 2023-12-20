import random
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render,redirect
from cart.models import Order,OrderItem,Coupon
from admin_dash.models import Variants
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .helpers import render_to_pdf
from .forms import *
from .models import *
from django.contrib import messages
from django.core.exceptions import ValidationError
import re
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import never_cache



# Create your views here.
# @login_required(login_url='log_in')
# def user_account(request) :
#     return render(request, 'user_account/user_dash.html')

@never_cache
@login_required(login_url='log_in')
def user_orders(request) :
    orders = Order.objects.filter(user=request.user).order_by('-id')
    context = {'orders':orders}
    return render(request, 'user_account/user_orders.html',context)

@never_cache
@login_required(login_url='log_in')
def view_order(request,t_no) :
    order = Order.objects.filter(tracking_no=t_no).filter(user=request.user).first()
    orderitems = OrderItem.objects.filter(order=order)
    context={
        'order':order,
        'orderitems':orderitems
    }
    return render(request,'user_account/view_single_order.html',context)


    
    

@never_cache    
@login_required(login_url='log_in')
def cancel_order(request, t_no):
    try:
        # Get the order
        order_item = get_object_or_404(Order, tracking_no=t_no)

        # Ensure user has a wallet
        user_wallet, created = Wallet.objects.get_or_create(user=request.user, defaults={'wallet': 0})
        
        if user_wallet is None:
            raise Exception("User wallet not found or could not be created.")

        order_items = OrderItem.objects.filter(order=order_item)

        for item in order_items:
            product = item.product
            variant = Variants.objects.filter(product=product).first()
            if variant:
                variant.quantity += item.quantity
                print('varian saved ')
                variant.save()

        if order_item.payment_mode == 'paid by razorpay' or order_item.payment_mode == 'paid by wallet':
            if user_wallet.wallet is None:
                user_wallet.wallet = 0  # Set wallet to 0 if it is None
            user_wallet.wallet += order_item.total_price
            user_wallet.save()

        if request.method == 'POST':
            cancel_reason = request.POST.get('cancel_reason', '')
            order_item.cancel_reason = cancel_reason
            order_item.save()
            messages.success(request, 'Order canceled successfully.')
        order_item.status = 'Cancel'
        order_item.save()
        return HttpResponseRedirect(reverse('user_orders'))

        # return render(request, 'your_template_name/cancel_order.html', {'order': order_item})

    except Order.DoesNotExist:
        return HttpResponse("Order not found.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)
    # ==========================================


@never_cache   
def return_order(request, t_no):
    order = get_object_or_404(Order, tracking_no=t_no)

    if request.method == 'POST':
        return_reason = request.POST.get('return_reason', '')
        order.return_reason = return_reason
        order.save()
        messages.success(request, 'Return request submitted successfully.')
    return redirect('user_orders')
   # return redirect('user_orders', tracking_no=t_no)
   # return redirect(reverse('user_orders', kwargs={'t_no': t_no}))
    # ==================================
    
# ================== USER WALLET =============
@never_cache
@login_required(login_url='log_in')
def user_wallet(request):
    coupons = Coupon.objects.filter(is_expired=False) 
    try:
        wallet_instance = Wallet.objects.get(user=request.user)
    except ObjectDoesNotExist:
        wallet_instance = Wallet.objects.create(user=request.user, wallet=None)

    context = {'wallet': wallet_instance,'coupons':coupons}
    return render(request, 'user_account/wallet_show.html', context)
    
@never_cache
@login_required(login_url='log_in')
def user_address(request) :
    new_address = Address.objects.all().order_by('-id')
    context = {
        'new_address':new_address
    }
    return render(request, 'user_account/user_address.html',context)

@never_cache
@login_required(login_url='log_in')
def edit_address(request,ad_id) :
    address = Address.objects.get(id=ad_id)
    context ={
        'address':address
    }

    return render(request, 'user_account/edit_address.html',context)

@never_cache
@login_required(login_url='log_in')
def update_address(request,ad_id) :
    if request.method == 'POST' :
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')

        if fname.strip()=='' or lname.strip()=='' or email.strip()=='' or phone.strip()=='' or address.strip()=='' or city.strip()=='' or state.strip()=='' or country.strip()=='' or pincode.strip()=='' :
            messages.error(request, "Fields cannot be empty!")
            return redirect('edit_address',ad_id=ad_id)

        new_address = Address.objects.get(id=ad_id)
        new_address.fname = fname
        new_address.lname = lname
        new_address.email = email
        new_address.city = city
        new_address.state = state
        new_address.country = country
        new_address.phone = phone
        new_address.address = address
        new_address.pincode = pincode
        new_address.save()
        messages.success(request, 'Your address has been updated successfully!')
        return redirect('user_address')
  
    return render(request, 'user_account/edit_address.html')


@never_cache
@login_required(login_url='log_in')
def delete_user_address(request, ad_id) :
    address = get_object_or_404(Address, id=ad_id) 
    address.delete()
    messages.success(request, "You address is deleted !")
    return redirect('user_address')
   

@never_cache
@login_required(login_url='log_in')
def account_details(request):
    user = request.user
    user_form = UserUpdateForm(instance=user)
    password_form = ChangePasswordForm()
    password_updated = False

    if request.method == 'POST':
        if 'update_info' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=user)
            if user_form.is_valid():
                # Custom username validation
                username = user_form.cleaned_data.get('username')
                if username.isdigit():
                    user_form.add_error('username', 'Username must not contain only digits.')

                # Check if the username already exists
                if User.objects.filter(username=username).exclude(id=user.id).exists():
                    user_form.add_error('username', 'Username already exists.')

                # Custom email validation
                email = user_form.cleaned_data.get('email')
                if User.objects.filter(email=email).exclude(id=user.id).exists():
                    user_form.add_error('email', 'Email already exists.')
                if not re.match(r'^\S+@\S+\.\S+$', email):
                    user_form.add_error('email', 'Please enter a valid email address.')

                if not user_form.errors:
                    user_form.save()
                    messages.success(request, 'User information updated successfully')
                    return redirect('account_details')
                else:
                    for field, errors in user_form.errors.items():
                        for error in errors:
                            messages.error(request, f'Error in {field}: {error}')

        if 'change_password' in request.POST:
            password_form = ChangePasswordForm(request.POST)
            if password_form.is_valid():
                current_password = password_form.cleaned_data['current_password']
                new_password = password_form.cleaned_data['new_password']

                if user.check_password(current_password):
                    user.set_password(new_password)
                    user.save()
                    password_updated = True
                    messages.success(request, 'Password updated successfully. Please log in.')
                    login_url = reverse('log_in')

                    return redirect(login_url)
                else:
                    messages.error(request, 'Current password is incorrect')

    context = {
        'user_form': user_form,
        'password_form': password_form,
        'password_updated': password_updated,
    }
    return render(request, 'user_account/account_details.html', context)



# ====================== DOWNLOAD INVOICE ================
@never_cache
def generate_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    invoice_number = str(random.randint(100000, 999999))


    context = {
        'order': order,
        'invoice_number':invoice_number,
       
    }
 

    pdf = render_to_pdf('pdfs/invoice.html', context)
    # if pdf:
    #     response = HttpResponse(pdf, content_type='application/pdf')
    #     filename =f"invoice_{order.id}.pdf"
    #     # content = "inline; filename='%s'" % filename
    #     content = 'inline; filename="%s"' % filename
    #     response['Content-Disposition'] = content
    #     return response
    # else:
    #     print("Error generating the PDF.")
    #     return HttpResponse("Error generating the invoice.")
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"invoice_{order.id}.pdf"
        content = 'inline; filename="%s"' % filename
        response['Content-Disposition'] = content
        return response
    else:
        print("Error generating the PDF.")
        return HttpResponse("Error generating the invoice.")