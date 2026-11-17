from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def register(request):
    if request.method == 'POST':
        a = request.POST['first_name']
        b = request.POST['last_name']
        c = request.POST['username']
        d = request.POST['email']
        e = request.POST['password']

        try:
            User.objects.get(username=c)
            return render(request,'register.html',{
                'error': 'Username already exists'
            })
        except User.DoesNotExist:
            user = User.objects.create(
                first_name=a,
                last_name=b,
                username=c,
                email=d,
            )
            user.set_password(e)
            user.save()   

        return redirect('login')
    return render(request,'register.html')


def login_(request):
    if request.method == 'POST':
        a = request.POST['username']
        b = request.POST['password']

        user = authenticate(request, username=a, password=b)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')

@login_required(login_url='login')
def logout_(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def profile(request):
    return render(request,'profile.html')