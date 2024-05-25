from django.shortcuts import render, redirect
from library.forms import CreateUserForm, LoginForm
from library.models import Customer
from django.db import IntegrityError
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'library/index.html')


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
