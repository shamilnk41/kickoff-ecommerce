from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import CreateUserForm
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
import re
from django.core.paginator import Paginator,EmptyPage, InvalidPage
from admin_dash.models import Product,Category,Brand,Variants,Banner
from django.core.exceptions import ObjectDoesNotExist
import pyotp
from datetime import datetime,timedelta
from django.http import HttpResponse


# Create your views here.

@never_cache
def sign_up(request):
    if request.user.is_authenticated:
        return render(request, 'base.html')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not first_name or not last_name or not username or not email or not password1 or not password2:
            messages.error(request, "Please fill in all the required fields.")
            return redirect('sign_up')
        if not first_name.isalpha():
            messages.error(request, "First name should only contain alphabetic characters.")
            return redirect('sign_up')
        
        if not last_name.isalpha():
            messages.error(request, "First name should only contain alphabetic characters.")
            return redirect('sign_up')

        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messages.error(request, "Please enter a valid email address.")
            return redirect('sign_up')
        
        if username.isdigit():
            messages.error(request, "Username should not only contain digits.")
            return redirect('sign_up')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken. Please choose another one.")
            return redirect('sign_up')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email address is already registered. Please use a different email.")
            return redirect('sign_up')

        if password1 != password2:
            messages.error(request, "Passwords do not match. Please enter the same password in both fields.")
            return redirect('sign_up')

        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('sign_up')

        # if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', password1):
        #     messages.error(request, "Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character.")
        #     return redirect('sign_up')
        
        if not re.match(r'^(?=.*[A-Z])[A-Za-z\d@$!%*?&]+$', password1):
            messages.warning(request, "For a stronger password, consider including at least one uppercase letter and additional characters.")
            return redirect('sign_up')
       

        
        user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
        user.save()
        request.session['email'] = email
        request.session['password'] = password1
        send_otp(request)
        return render(request, 'user/otp.html', {'email': email})

    return render(request, 'user/sign_up.html')


# def log_in(request) :

#     if request.method == 'POST' :
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         username = User.objects.get(email=email.lower()).username
#         user = authenticate(request, username=username, password=password)
#         if user is not None :
#             login(request, user)
#             return render(request, 'base.html')
#         else :
#             messages.error(request, 'Oops.. Bad credentials!')
#     return render(request, 'user/log_in.html')
# 
#     
@never_cache
def log_in(request):
    if request.user.is_authenticated:
        return render(request, 'base.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            username = User.objects.get(email=email.lower()).username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in')
                return redirect('home')
            else:
                messages.error(request, 'Oops.. Bad credentials!')
        except ObjectDoesNotExist:
            messages.error(request, 'User with this email does not exist')
    return render(request, 'user/log_in.html')


@never_cache
def log_out(request):
    if request.user.is_authenticated:
        request.session.flush()  # Clear the entire session
        logout(request)
        messages.success(request, "You are logged out!")
    else:
        # Handle the case when the user is not authenticated (optional)
        messages.warning(request, "You are not logged in.")

    return redirect('home')
# @never_cache
# def log_out(request) :
#     if 'username' in request.session :
#         del request.session['username']
#     logout(request)
#     messages.success(request, "You are logged out !")
#     return redirect('home')

# @login_required(login_url='log_in')
# @never_cache
# def log_out(request):
#     if 'username' in request.session:
#         del request.session['username']


def send_otp(request):
    totp_secret_key = pyotp.random_base32()
    totp = pyotp.TOTP(totp_secret_key, interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp_secret_key  
    request.session['otp_valid_date'] = str(datetime.now() + timedelta(minutes=1))
    request.session['otp'] = otp  

    email_template = 'user/email_otp.html'
    html_message = render(request, email_template, {'otp': otp}).content.decode('utf-8')

    # send_mail("OTP for sign up", otp, 'shamilnk0458@gmail.com', [request.session['email']], fail_silently=False)
    send_mail(
        subject="OTP for Sign Up",
        message="",  # Leave this empty as you are sending HTML content
        from_email='shamilnk0458@gmail.com',
        recipient_list=[request.session['email']],
        html_message=html_message,
        fail_silently=False
    )
    print('otp send 1st')
    return render(request, 'user/otp.html')




def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        stored_otp = request.session.get('otp')  # Retrieve the stored OTP
        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_date = request.session.get('otp_valid_date')

        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)

            if valid_until > datetime.now():
                if entered_otp == stored_otp:
                    email = request.session['email']
                    password = request.session['password']
                    username = User.objects.get(email=email.lower()).username
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('home')
                else:
                    messages.error(request, "Invalid OTP. Please enter a valid OTP.")
            else:
                messages.error(request, "OTP has expired. Please request a new OTP.")
        else:
            messages.error(request, "OTP validation failed. Please request a new OTP.")
    return render(request, 'user/otp.html')



def resend_otp(request):
   
    totp_secret_key = pyotp.random_base32()
    totp = pyotp.TOTP(totp_secret_key, interval=60)
    otp = totp.now()
    request.session['otp_secret_key'] = totp_secret_key
    request.session['otp_valid_date'] = str(datetime.now() + timedelta(minutes=1))
    request.session['otp'] = otp


    send_mail("Resent OTP for sign up", otp, 'shamilnk0458@gmail.com', [request.session['email']], fail_silently=False)
    messages.success(request, "OTP has been resent. Please check your email.")
    return render(request, 'user/otp.html')

# ==============  FORGOT PASSWORD ===========
@never_cache
def forgot_password_main(request) :
    return render(request, 'user/forgot_password.html')

@never_cache
def home(request) :
    all_products = Product.objects.filter(is_available =True).order_by('-id')[:8]
    banner = Banner.objects.filter(is_available=True).order_by('-id').first()
    banner_2 = Banner.objects.filter(is_available=True).order_by('-id')[1]
    return render(request, 'base.html',{'all_products':all_products,'banner':banner,'banner_2':banner_2})

@never_cache
def show_single_product(request,product_id) :
    # product = Product.objects.filter(id=product_id).first()
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(categories=product.categories).exclude(id=product_id)[:4]

    context = {
        'product':product,
        'related_products':related_products,
    }
    return render(request, 'single_product.html',context)

@never_cache
def store(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    category = None 
    brand = None
    cate_id = request.GET.get('categories')
    brand_id = request.GET.get('brand') 
    # price_range = request.GET.get('price_range') 

    if brand_id and brand_id != 'None':
        products = products.filter(brand__id=brand_id)
        brand = products

    if cate_id and cate_id != 'None':
        category = get_object_or_404(Category, id=cate_id)
        products = Product.objects.filter(categories=category)

    # if price_range and '-' in price_range:
    #     try:
    #         min_price, max_price = map(int, price_range.split('-'))
    #         products = products.filter(price__range=(min_price, max_price))
    #     except ValueError:
    #         pass

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    all_products = paginator.get_page(page_number)

    context = {
        'categories': categories,
        'all_products': all_products,
        'brands': brands,
        # 'filter_price': filter_price,
        'brand_id': brand_id,
        'cate_id': cate_id,
        'category': category, 
        'brand': brand,
        # 'price_range': price_range, 
    }

    return render(request, 'store.html', context)

@never_cache
def search_products(request):
    query = request.GET.get('query')
    categories = Category.objects.all()
    brands = Brand.objects.all()
    filter_price = Filter_price.objects.all()
    # category = None
    # brand = None
    # cate_id = request.GET.get('categories')
    # brand_id = request.GET.get('brand')
    # price_range = request.GET.get('price_range')

    products = Product.objects.all()  

    if query:  
        products = products.filter(name__icontains=query)

    # if brand_id and brand_id != 'None':
    #     brand = get_object_or_404(Brand, id=brand_id)
    #     products = products.filter(brand=brand)

    # if cate_id and cate_id != 'None':
    #     category = get_object_or_404(Category, id=cate_id)
    #     products = products.filter(categories=category)

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')

    try:
        all_products = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        all_products = paginator.page(1)

    context = {
        'categories': categories,
        'all_products': all_products,
        'brands': brands,
        # 'filter_price': filter_price,
        # 'brand_id': brand_id,
        # 'cate_id': cate_id,
        # 'category': category,
        # 'brand': brand,
        # 'price_range': price_range,
    }
    return render(request, 'search_products.html', context)
