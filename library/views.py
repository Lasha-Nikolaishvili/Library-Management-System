from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404
from library.forms import CreateUserForm, LoginForm
from library.models import Customer, Book
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'library/index.html')


def books_listing(request):
    if request.GET.get('filter'):
        filter_property: str = request.GET.get('filter')
        books = Book.objects.filter(
            Q(title__icontains=filter_property) |
            Q(authors__full_name__icontains=filter_property)
        ).distinct()
    else:
        books = Book.objects.all()
    paginator = Paginator(books, 8)
    page_num = int(request.GET.get('page', 1))
    page = paginator.get_page(page_num)

    return render(request, 'library/books.html', {'page': page})


def top_ten_books(request):
    books = (
        Book.objects
        .annotate(checkout_count=Count('checkout'))
        .order_by('-checkout_count')[:10]
        # .values('id', 'title', 'image', 'checkout_count')
    )
    print(books)

    return render(request, 'library/top_ten_books.html', {'books': books})


def book_details(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    authors = book.authors.all()
    genres = book.genres.all()

    context = {'book': book, 'authors': authors, 'genres': genres}
    return render(request, 'library/book_details.html', context=context)


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            try:
                user = form.save(commit=False)
                email = form.cleaned_data.get('email')
                full_name = form.cleaned_data.get('full_name')
                personal_number = form.cleaned_data.get('personal_number')
                birth_date = form.cleaned_data.get('birth_date')

                user.first_name = full_name.split()[0]
                user.last_name = ' '.join(full_name.split(' ')[1:])
                user.save()

                customer = Customer.objects.create(
                    user=user,
                    email=email,
                    full_name=full_name,
                    personal_number=personal_number,
                    birth_date=birth_date
                )
                customer.save()
                return redirect('library:login')
            except IntegrityError:
                form.add_error('personal_number', 'A customer with this personal number already exists.')
                user.delete()

    context = {'form': form}
    return render(request, 'library/register.html', context=context)


def login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
                return redirect('library:dashboard')
            else:
                form.add_error('username', 'Email or password is incorrect.')

    context = {'form': form}

    return render(request, 'library/login.html', context=context)


def logout(request):
    auth_logout(request)
    return redirect('library:index')


@login_required(login_url='library:login')
def dashboard(request):
    return render(request, 'library/dashboard.html')
