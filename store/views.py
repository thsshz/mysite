
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Store, Review
from .forms import StoreForm, ReviewForm

# Create your views here.


def index(request):
    stores = Store.objects.all()
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


def review(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = store.reviews.all()
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '全部', 'path': request.get_full_path()})


def review_sort(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = Review.objects.filter(store__id=store_id)
    if request.POST['review-order'] == 'latest':
        reviews = reviews.order_by('-create_at')
    elif request.POST['review-order'] == 'oldest':
        reviews = reviews.order_by('create_at')
    elif request.POST['review-order'] == 'likest':
        reviews = reviews.order_by('like')
    path = request.get_full_path()
    path = path[:-5]
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '全部', 'path': path})


def review_5star(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = Review.objects.filter(star=5, store__id=store.id)
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '5星', 'path': request.get_full_path()})


def review_5star_sort(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = Review.objects.filter(star=5, store__id=store_id)
    if request.POST['review-order'] == 'latest':
        reviews = reviews.order_by('-create_at')
    elif request.POST['review-order'] == 'oldest':
        reviews = reviews.order_by('create_at')
    elif request.POST['review-order'] == 'likest':
        reviews = reviews.order_by('like')
    path = request.get_full_path()
    path = path[:-5]
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '5星', 'path': path})


def review_4star(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = Review.objects.filter(star=4, store__id=store.id)
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '4星', 'path': request.get_full_path()})


def review_4star_sort(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = Review.objects.filter(star=4, store__id=store_id)
    if request.POST['review-order'] == 'latest':
        reviews = reviews.order_by('-create_at')
    elif request.POST['review-order'] == 'oldest':
        reviews = reviews.order_by('create_at')
    elif request.POST['review-order'] == 'likest':
        reviews = reviews.order_by('like')
    path = request.get_full_path()
    path = path[:-5]
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '4星', 'path': path})


def review_3star(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = Review.objects.filter(star=3, store__id=store.id)
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '3星', 'path': request.get_full_path()})


def review_3star_sort(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = Review.objects.filter(star=3, store__id=store_id)
    if request.POST['review-order'] == 'latest':
        reviews = reviews.order_by('-create_at')
    elif request.POST['review-order'] == 'oldest':
        reviews = reviews.order_by('create_at')
    elif request.POST['review-order'] == 'likest':
        reviews = reviews.order_by('like')
    path = request.get_full_path()
    path = path[:-5]
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '3星', 'path': path})


def review_2star(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = Review.objects.filter(star=2, store__id=store.id)
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '2星', 'path': request.get_full_path()})


def review_2star_sort(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = Review.objects.filter(star=2, store__id=store_id)
    if request.POST['review-order'] == 'latest':
        reviews = reviews.order_by('-create_at')
    elif request.POST['review-order'] == 'oldest':
        reviews = reviews.order_by('create_at')
    elif request.POST['review-order'] == 'likest':
        reviews = reviews.order_by('like')
    path = request.get_full_path()
    path = path[:-5]
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '2星', 'path': path})


def review_1star(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = Review.objects.filter(star=1, store__id=store.id)
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '1星', 'path': request.get_full_path()})


def review_1star_sort(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    reviews = Review.objects.filter(star=1, store__id=store_id)
    if request.POST['review-order'] == 'latest':
        reviews = reviews.order_by('-create_at')
    elif request.POST['review-order'] == 'oldest':
        reviews = reviews.order_by('create_at')
    elif request.POST['review-order'] == 'likest':
        reviews = reviews.order_by('like')
    path = request.get_full_path()
    path = path[:-5]
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '1星', 'path': path})


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
