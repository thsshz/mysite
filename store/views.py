from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Store
from .forms import StoreForm, ReviewForm

# Create your views here.


def index(request):
    stores = Store.objects.all()
    return render(request, 'index.html', {'stores': stores})


def index_5star(request):
    stores = Store.objects.filter(star=5)
    return render(request, 'index.html', {'stores': stores})





def create(request):
    params = request.POST if request.method == 'POST' else None
    form = StoreForm(params)
    if form.is_valid():
        store = form.save(commit=False)
        store.review_number = 0
        store.save()
        messages.info(request, '店铺“{}”添加成功'.format(store.name))
        form = StoreForm()

    return render(request, 'create.html', {'form': form})


def store(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    return render(request, 'store.html', {'store': store, 'review_form': ReviewForm()})


@require_POST
def write_review(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.store = store
        review.like = 0
        print(review.save())
        messages.info(request, '您为商家{}填写的评论发表成功'.format(store.name))
    else:
        print('not valid')
        messages.warning(request, '评论发表失败')

    return redirect('store', store.id)
