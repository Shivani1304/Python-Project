from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Publisher, Book, Member, Order, Review
from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
from .forms import SearchForm, ReviewForm,OrderForm,MemberForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from random import randint
from django.template.loader import render_to_string
from datetime import datetime

def index(request):
    last_login = "";
    if request.session.has_key('last_login'):
        last_login = request.session['last_login']
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist, 'last_login':last_login})

def about(request):
    response = HttpResponse()
    if 'number' in request.COOKIES:
        mynum = request.COOKIES['number']
    else:
        mynum = randint(1, 100)
        response.set_cookie('number', mynum, 10)
    fav_number = render_to_string('myapp/about.html', {'mynum': mynum})
    response.write(fav_number)
    return response

def detail(request,book_id):
        book = get_object_or_404(Book,id = book_id)
        return render(request, 'myapp/detail.html', {'book': book})

def findbooks(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['your_name']
                category = form.cleaned_data['select_a_category']
                price = form.cleaned_data['maximum_price']
                #booklist = Book.objects.filter(category= category, price=price)
                booklist = Book.objects.filter(price__lte = price, category= category)
                booklist1 = Book.objects.filter(price__lte=price)
                return render(request, 'myapp/results.html', {'booklist':booklist, 'your_name':name,'select_a_category': category, 'booklist1':booklist1})
            else:
                return HttpResponse('Invalid data')
        else:
            form = SearchForm()
            return render(request, 'myapp/findbooks.html', {'form':form})
    else:
        request.session['fb'] = 'findbooks'
        return render(request, 'myapp/login.html')

def place_order(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = OrderForm(request.POST)
            if form.is_valid():
                books = form.cleaned_data['books']
                order = form.save(commit=True)
                member = order.member
                type = order.order_type
                total = 0
                order.save()
                if type == 1:
                    for b in order.books.all():
                        member.borrowed_books.add(b)

                    for b1 in books:
                        total=total+b1.price

                return render(request, 'myapp/order_response.html', {'books': books, 'order':order, 'total': total})
            else:
                return render(request, 'myapp/placeorder.html', {'form':form})

        else:
            form = OrderForm()
            return render(request, 'myapp/placeorder.html', {'form':form})
    else:
        request.session['po'] = 'place_order'
        return render(request, 'myapp/login.html')

def review(request):
    if request.user.is_authenticated:
        if request.user.member.status == 3:
            return HttpResponse("You are not authorize to review")
        if request.method == 'POST':
            form = ReviewForm(request.POST)
            if form.is_valid():
                rating = form.cleaned_data['rating']
                if rating >= 1 and rating <= 5:
                    reviewer = form.cleaned_data['reviewer']
                    book = form.cleaned_data['book']
                    comments = form.cleaned_data['comments']
                    review = form.save(commit= True)
                    review.save()
                    book = review.book
                    book.num_reviews+=1
                    return index(request)

                else:
                    ratingerr = 'Please rate book between 1 and 5!'
                    return render(request, 'myapp/review.html', {'form':form, 'ratingerr':ratingerr})
            else:
                #request.session['login'] = 'review'
                #return render(request, 'myapp/login.html')
                return render(request,'myapp/review.html',{'form': form})

        else:
            form = ReviewForm()
            return render(request, 'myapp/review.html', {'form':form})
    else:
        request.session['rv'] = 'review'
        return render(request, 'myapp/login.html')

def user_login(request):
    if request.method == 'POST':
        #valuenext = request.POST.get('next')
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                request.session.set_expiry(3600)
                request.session['username'] = username
                login(request,user)
                #redirect to review page
                if 'rv' in request.session:
                    return HttpResponseRedirect(reverse('myapp:review'))
                # redirect to finds books page
                elif 'fb' in request.session:
                    return HttpResponseRedirect(reverse('myapp:findbooks'))
                # redirect to place order page
                elif 'po' in request.session:
                    return HttpResponseRedirect(reverse('myapp:place_order'))
                #redirect to chk_reviews
                elif request.session.get('redirect', False):
                    resp = HttpResponseRedirect(request.session['redirect'])
                    return resp
                else:
                    return HttpResponseRedirect(reverse('myapp:index'))

            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

def register(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            current_login_time = str(datetime.datetime.now())
            request.session['last_login'] = current_login_time
            request.session['username'] = username
            return redirect('myapp:index')
            # form = RegisterForm()
            # return render(request, 'myapp/register.html', {'form': form})
    else:
        form = MemberForm()
        return render(request, 'myapp/register.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))

# redirect to login page
def chk_reviews(request,book_id):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, id=book_id)
        reviews = Review.objects.filter(book_id=book_id)
        rating = 0
        avg = 0
        for r in reviews:
            rating += r.rating
            avg += 1
        if avg > 0:
            rating /= avg
            return render(request, 'myapp/chk_reviews.html', {'book': book, 'average_rating': avg})
        else:
            return HttpResponse('No ratings available.')
    else:
        request.session['redirect'] = request.path
        request.session.save()
        return render(request, 'myapp/login.html')

