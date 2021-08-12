from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contacts


def register(request):
    if request.method == "POST":
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check passwords
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'This user name has already been taken!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'User with the same email already exists!')
                    return redirect('register')
                else:
                    # Everything looks good for registration
                    user = User.objects.create_user(username=username, email=email, password=password,
                                                    first_name=first_name, last_name=last_name)
                    # Login after successful registration
                    # auth.login(request, user)
                    # messages.success(request, 'You are now logged in!')
                    # return redirect('index')
                    user.save()
                    messages.success(request, 'You are successfully registered and can log in.')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == "POST":

        # Get username and password
        username = request.POST['username']
        password = request.POST['password']

        # Check if user gets authenticated
        user = auth.authenticate(username=username, password=password)

        # If user is found, login
        # If not, post error message
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Credentials you entered are incorrect!')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def dashboard(request):
    user_contacts = Contacts.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)


def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, 'You are logged out!!')
        return redirect('index')

