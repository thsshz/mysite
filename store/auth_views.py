from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Store, Review, Area, Category, Client

def login(request):
    return render(request, 'login.html')

def authenticate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(request, username=username, password=password)

    if not user:
        return redirect('login')

    auth.login(request, user)
    return redirect('index')

def signup(request):
    return render(request, 'signup.html')

def signup_submit(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = User.objects.create_user(username=username, password=password)
        client = Client()
        client.user = user
        client.save()
        return redirect('login')
    except:
        return redirect('signup')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

#likestore
def likestore(request, user_id, store_id):
    user = User.objects.filter(id=user_id)[0]
    print(1)
    client = Client.objects.filter(user=user)[0]
    print(2)
    store = Store.objects.filter(id=store_id)[0]
    print(3)
    client.like_stores.add(store)
    print(4)
    client.save()
    return redirect('store', store_id)

def client(request):
    return render(request, 'client.html')
