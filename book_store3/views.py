from django.shortcuts import render,redirect, HttpResponse,get_object_or_404
from book_store3.models import *
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
def home(request):

    home = mostsell.objects.all()
    return render(request, 'home.html', {'home': home})

def booklist(request):

    category=request.GET.get('category')
    bookauthor=request.GET.get('bookauthor')
    language=request.GET.get('language')
    genre = request.GET.get('genre')
    search = request.GET.get('search')
    if category:
        page_obj= Product.objects.filter(category_id=category)
    
    elif bookauthor:
        page_obj= Product.objects.filter(bookauthor_id=bookauthor)

    elif language:
        page_obj= Product.objects.filter(language_id=language)
    
    elif genre:
        page_obj= Product.objects.filter(genre_id=genre)
    

    elif search:
        page_obj= Product.objects.filter(
            Q(name__icontains=search)|
            Q(content__icontains=search)|
            Q(category__name__icontains=search)|
            Q(bookauthor__name__icontains=search)|
            Q(language__name__icontains=search)|
            Q(genre__icontains=search)
        )
    else:
        posts = Product.objects.all().order_by('-created_at')
        paginator=Paginator(posts,4)
        page_number=request.GET.get('page')
        page_obj=paginator.get_page(page_number)
    return render(request, 'booklist.html',{'posts':page_obj})

def navigate(request):
    context = {}
    return render(request, 'navegate.html', context)

@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None

    context = {
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)

@login_required
def userprofile_create(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        address = request.POST.get('address')
        dob = request.POST.get('dob')

        if not image or not address or not dob:
            messages.error(request, "All fields are required.")
            return redirect('/profile')

        UserProfile.objects.create(
            user=request.user,
            image=image,
            address=address,
            dob=dob,
        )
        messages.success(request, "Profile successfully added!")
        return redirect('/profile')

    return render(request, 'userprofile_create.html')

@login_required
def userprofile_edit(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('/profile')

    if request.method == 'POST':
        image = request.FILES.get('image')
        address = request.POST.get('address')
        dob = request.POST.get('dob')

        if not address or not dob:
            messages.error(request, "Address and Date of Birth are required.")
            return redirect('/profile/edit')

        user_profile.address = address
        user_profile.dob = dob
        if image:
            user_profile.image = image
        user_profile.save()

        messages.success(request, "Profile successfully updated!")
        return redirect('/profile')

    formatted_dob = user_profile.dob.strftime('%Y-%m-%d') if user_profile.dob else ''

    context = {
        'user_profile': user_profile,
        'formatted_dob': formatted_dob,
    }
    return render(request, 'userprofile_edit.html', context)
    

@permission_required('b_store.add_post', login_url='login')
def bookcreate(request):

    if request.method == 'GET':
        category=Category.objects.all()
        language=Language.objects.all()
        bookauthor=Author.objects.all()
        return render(request, 'bookcreate.html', {'category': category, 'language': language, 'bookauthor': bookauthor,})
        
    if request.method == 'POST':
        Product.objects.create(
            name = request.POST.get('name'),
            content = request.POST.get('content'),
            image = request.FILES.get('image'),
            category_id = request.POST.get('category'),
            genre= request.POST.get('genre'), 
            language_id= request.POST.get('language'),
            bookauthor_id=request.POST.get('bookauthor'),
            price = request.POST.get('price'),
            qty = request.POST.get('quantity'),
        )
        messages.success(request, "Book successfully added!")
        return redirect('/book/list')
    
@permission_required('b_store.delete_post', login_url='login')
def bookdelete(request, b_id):
    post = Product.objects.get(id=b_id)
    post.image.delete()
    post.delete()
    messages.success(request, "Book Deleted Success!")
    return redirect('/book/list')

@permission_required('b_store.change_post', login_url='login')
def bookedit(request, b_id):

    if request.method == "GET":
        post = Product.objects.get(id=b_id)
        category = Category.objects.all()
        language = Language.objects.all()
        bookauthor = Author.objects.all()
        return render(request, 'bookedit.html', {'p':post,'category':category,'language':language,'bookauthor':bookauthor})
    if request.method == "POST":
        post = Product.objects.get(id=b_id)
        post.name = request.POST.get('name')
        post.content = request.POST.get('content')
        if request.FILES.get('image'):
            post.image.delete()
            post.image = request.FILES.get('image')
        post.category_id = request.POST.get('category')
        post.genre = request.POST.get('genre')
        post.language_id = request.POST.get('language')
        post.bookauthor_id = request.POST.get('bookauthor')
        post.price = float(request.POST.get('price'))
        post.qty = float(request.POST.get('quantity'))  

        post.save()
        messages.success(request, "Post Updated Success!")
        return redirect('/book/list')

def bookdetail(request, b_id):
    if request.method == 'GET':
        post=Product.objects.get(id=b_id)
        return render(request,'bookdetail.html',{'p':post})
    if request.method == 'POST':
        if request.user.username == '':
            return redirect('/login')
        
@login_required        
def CartCreate(request, pdt_id):
    carts = Cart.objects.filter(user_id=request.user.id)
    qty = request.GET.get('qty')
    for item in carts:
        if item.product_id == pdt_id:
            item.qty = item.qty + int(qty)
            item.created_at = datetime.now()
            item.save()
            print(serializers.serialize('json', [ item, ]))
            messages.success(request, f"Added {qty} {item.product.name} successfully.")
            return redirect(f'/book/list/')
    cart = Cart.objects.create(
        product_id = pdt_id,
        qty = qty,
        user_id = request.user.id,
        created_at = datetime.now()
    )
    messages.success(request, f"Added {qty} {cart.product.name} successfully.")
    return redirect(f'/book/list/')

def CartList(request):
    cart = Cart.objects.filter(user_id=request.user.id).order_by('-created_at')
    for item in cart:
        item.total = item.product.price * item.qty
    return render(request, 'cartList.html',{'cart':cart})

def CartDelete(request,cart_id):
    cart = Cart.objects.get(id=cart_id)
    cart.delete()
    messages.success(request, f"Deleted {cart.product.name} successfully.")
    return redirect(f'/book/cartList/')

@login_required
def buyNow(request,post_id):
    product = Product.objects.get(id = post_id)
    product.qty = request.GET.get('qty')
    product.total = product.price * int(product.qty)
    if request.method == "GET":
        return render(request, 'orderCreate.html',{'product':product})
    if request.method == "POST":
        Myproduct = []
        Myproduct.append({
            'id':product.id, 
            'image':product.image.url,
            'name':product.name, 
            'price':product.price, 
            'qty':product.qty, 
            'total':product.total
            }) 
        order = Order.objects.create(
            product = Myproduct,
            user_id = request.user.id,
            total_price = product.total,
            total_qty = product.qty,
            name = request.POST.get('name'),
            phone = request.POST.get('phone'),
            address = request.POST.get('address'),
            created_at = datetime.now()
        )
        messages.success(request, "Order successfully.")
        return redirect(f'/book/list/')
    
def cartOrderCreate(request):
    cart = Cart.objects.filter(user_id=request.user.id)
    product = []
    total = 0
    total_qty = 0
    for c in cart:
        product.append({
            'id':c.product.id, 
            'image':c.product.image.url,
            'name':c.product.name, 
            'price':c.product.price, 
            'qty':c.qty, 
            'total':c.product.price * c.qty
            })
        total += c.product.price * c.qty
        total_qty += c.qty
    order = Order.objects.create(
        product = product,
        user_id = request.user.id,
        total_price = total,
        total_qty = total_qty,
        name = request.POST.get('name'),
        phone = request.POST.get('phone'),
        address = request.POST.get('address'),
        created_at = datetime.now()
    )
    cart.delete()
    messages.success(request, "Order successfully.")
    return redirect(f'/book/list/')

def orderList(request):
    orders = Order.objects.filter(user_id = request.user.id).order_by('-created_at')
    return render(request, 'orderList.html',{'orders':orders})

def orderDelete(request,order_id):
    orders = Order.objects.get(id=order_id)
    orders.delete()
    messages.success(request, f"Deleted successfully.")
    return redirect(f'/book/orderList/')


def bookcontact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('ph')
        message = request.POST.get('msg')
        author_id = request.user.id
        
        feedback = Feedback(name=name, phone=phone, message=message, author_id=author_id)
        feedback.save()

        messages.success(request, "Feedback submitted successfully.")
        return redirect('contact')  
    else:
        return render(request, 'contact.html')

      
def mylogin(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login Success!")
            return redirect('/book/list')
        else:
            messages.error(request, "Username Or Password is Incorrect!")
            return redirect('/login')
        
def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            return redirect('reset_password', user_id=user.id)
        else:
            messages.error(request, "Username not found.")
            return redirect('forgot_password')
    return render(request, 'forgot_password.html')

def reset_password(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        new_password = request.POST.get('password')
        user.set_password(new_password)
        user.save()
        messages.success(request, "Password has been reset successfully.")
        return redirect('login')
    return render(request, 'reset_password.html', {'user_id': user_id})
        
def mylogut(request):
    logout(request)
    return redirect('/book/list')

def myregister(request):
    if request.method == "GET":
        return render(request,'register.html')
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        if password == repassword:
            if User.objects.filter(username=username):
                messages.error(request, 'username already exists')
                return redirect('/register')
            if User.objects.filter(email=email):
                messages.error(request, 'email already exists')
                return redirect('/register')
            user=User.objects.create(
                username = username,
                email = email,
                password = make_password(password)
            )
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('/')
        else:
            messages.error(request, 'Password is not same!')
            return redirect('/register')
        

        
def pagenotfound(request):
    return render(request,'404.html')