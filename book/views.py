from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from . models import Book,Rental,User
from math import ceil
from django.db.models import Sum
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
import razorpay
from django.views.decorators.csrf import csrf_exempt

def index(request):
    allBooks = []
    catprods = Book.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Book.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allBooks.append([prod, range(1, nSlides), nSlides])
    params = {'allBooks':allBooks}
    return render(request, 'book/index.html',params)


@login_required
def rental(request, title):
    user = request.user
    book = get_object_or_404(Book, title=title)
    if request.method == 'POST':
        rental_date = request.POST.get('rental_date')
        return_date = request.POST.get('return_date')
        if rental_date and return_date:
            rental_date = timezone.datetime.strptime(rental_date, "%Y-%m-%d").date()
            return_date = timezone.datetime.strptime(return_date, "%Y-%m-%d").date()
            months_rented = (return_date - rental_date).days // 30
            if months_rented > 1:
                fee = book.page_count / 100 * (months_rented - 1)
            else:
                fee = 0.00
        else:
            fee = 0.00
        rental = Rental(user=user, book=book, rental_date=rental_date, return_date=return_date,fee=fee)
        rental.save()
        messages.success(request, "Your Book  has been successfully rent please check Checkout")
    return render(request, 'book/rental.html', {'user': user, 'book': book})

@login_required
def checkout(request):
    if request.method == 'POST':
        rental_id = request.POST.get('rental_id')
        rental = Rental.objects.get(pk=rental_id)
        rental.delete()
        return redirect('checkout')

    user = request.user
    rented_books = Rental.objects.filter(user=user)
    total_bill = rented_books.aggregate(Sum('fee'))['fee__sum'] or 0 
    return render(request, 'book/checkout.html', {'rented_books': rented_books, 'total_bill': total_bill})

def initiate_payment(request):
    if request.method == "POST":
        user = request.user
        rented_books = Rental.objects.filter(user=user)
        total_bill_usd = rented_books.aggregate(Sum('fee'))['fee__sum'] or 0  
        exchange_rate = 75
        total_price_inr = total_bill_usd / exchange_rate
        total_price = int(total_price_inr * 100)

        client = razorpay.Client(
             auth=("rzp_test_p4BF3I5vEzR2EV", "4hQaHiYf7Yxogxp5NBIeFeiy"))

        payment = client.order.create({'amount': total_price*100, 'currency': 'INR',
                                       'payment_capture': 1})

        if request.user.is_authenticated:
            rented_books.delete()
        return render(request, "book/payment.html",{'total_bill':total_bill_usd, 'payment':payment})
    return render(request, "book/payment.html")

@csrf_exempt
def success(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        client = razorpay.Client(
            auth=("rzp_test_p4BF3I5vEzR2EV", "4hQaHiYf7Yxogxp5NBIeFeiy")
        )
        params_dict = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        }
        try:
            client.utility.verify_payment_signature(params_dict)
            if request.user.is_authenticated:
                rented_books = Rental.objects.filter(user=request.user)
                rented_books.delete()
            return redirect("success")
        except:
            messages.error(request, "Payment failed. Please try again.")
            return redirect("checkout")
    return render(request, "book/success.html")
      
def Registers(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        firstName = request.POST['first--name']
        lastName = request.POST['last--name']
        username = request.POST['username'] 
        User = get_user_model()
        if User.objects.filter(email=email).exists():
            messages.info(request,'User already exists')
            return render(request, 'register.html')
        else:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=firstName, last_name=lastName, is_user=True)
            return redirect('login')
    else:
        return render(request, 'book/register.html')
       
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
 
        user = auth.authenticate(username=username, password=password)
 
        if user is not None and user.is_user:
            if user.is_admin:
                messages.info(request, 'Admins cannot login here.')
                return render(request, 'book/login.html')
            auth.login(request, user)
            print('User logged in successfully')
            return redirect('/')
        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'book/login.html')
    else:
        return render(request, 'book/login.html')
  

def Logout(request):
    auth.logout(request)
    return redirect('index')

def search_book(request):
    if 'title' in request.GET:
        title = request.GET['title']
        response = requests.get(f'https://openlibrary.org/search.json?title={title}')
        data = response.json()
        if data['docs']:
            book_data = data['docs'][0]
            cover_id = book_data.get('cover_i')
            if cover_id:
                cover_url = f"http://covers.openlibrary.org/b/id/{cover_id}-L.jpg"
            else:
                cover_url = 'N/A' 
            isbn_list = book_data.get('isbn', ['N/A'])
            isbn = isbn_list[0] if isbn_list else 'N/A'
            book = {
                'title': book_data.get('title', 'N/A'),
                'author': ', '.join(book_data.get('author_name', ['N/A'])),
                'page_count': book_data.get('number_of_pages_median', 'N/A'),
                'isbn': isbn,
                'cover_url': cover_url 
            }
            latest_books = request.session.get('latest_books', [])
            if book not in latest_books:
                latest_books.insert(0, book)
                request.session['latest_books'] = latest_books
                messages.success(request, "Book added successfully to the latest books list.")
            else:
                messages.info(request, "The book is already in the latest books list.") 
            return render(request, 'book/search_book.html', {'book': book})
    return render(request, 'book/search_book.html', {'book': None})

def latest_books(request):
    latest_books = request.session.get('latest_books', [])
    return render(request, 'book/latest_books.html', {'latest_books': latest_books})

def delete_book(request):
    if request.method == 'POST':
        book_title = request.POST.get('book_title')
        latest_books = request.session.get('latest_books', [])
        updated_books = [book for book in latest_books if book['title'] != book_title]
        request.session['latest_books'] = updated_books
        request.session.modified = True
    return redirect('latest_books')

