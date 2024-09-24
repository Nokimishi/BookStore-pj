from book_store3.models import Category,Language,Author,Cart

def category(request):
    category = Category.objects.all()
    return {'cat':category}

def language(request):
    language = Language.objects.all()
    return {'lag':language}

def BookAuthor(request):
    bookauthor = Author.objects.all()
    return {'aut':bookauthor}

def cartCount(request):
    count = Cart.objects.filter(user_id=request.user.id).count()
    return {'count':count}


