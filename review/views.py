from django.shortcuts import render
from .models import Review

# Create your views here.


def index(request):
    reviews = Review.objects.order_by('-create_at')
    return render(request, 'index.html', {'reviews': reviews})
