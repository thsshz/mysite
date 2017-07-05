
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Store, Review, Area, Category
from .forms import StoreForm, ReviewForm
from .allstore import get_stores, AllStore
import re

# Create your views here.
def load_area_category(request):
    stores = Store.objects.all()
    areas = Area.objects.all()
    categories = Category.objects.all()
    for store in stores:
        if areas.filter(name__exact=store.area).count() == 0:
            area = Area()
            area.name = store.area
            area.state = False
            area.num = 0
            area.save()
        if categories.filter(name__exact=store.category).count() == 0:
            category = Category()
            category.name = store.category
            category.state = False
            category.num = 0
            category.save()
    return redirect('index')

def index(request):
    areas = Area.objects.all()
    for area in areas:
        area.state = False
        num_t = Store.objects.filter(area__exact=area.name).count()
        area.num = num_t
        area.save()
    categories = Category.objects.all()
    for category in categories:
        category.state = False
        num_t = Store.objects.filter(category__exact=category.name).count()
        category.num = num_t
        category.save()
    stores = get_stores(request)
    order_by_dic = AllStore.order_by_dic
    store_list = stores
    paginator = Paginator(store_list, 20)
    page = request.GET.get('page')
    try:
        stores_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        stores_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        stores_page = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'areas': areas, 'categories': categories, 'stores_page': stores_page, 'order_by_dic':order_by_dic, 'order_by_get':'star', 'per_consume_min':-1, 'per_consume_max':-1}) 

def area_index(request, area_id):
    setarea = Store.objects.filter(id=area_id)[0].area
    areas = Area.objects.all()
    for area in areas:
        area.state = False
        num_t = Store.objects.filter(area__exact=area.name).count()
        area.num = num_t
        area.save()
    categories = Category.objects.all()
    for category in categories:
        category.state = False
        num_t = Store.objects.filter(category__exact=category.name).count()
        category.num = num_t
        category.save()
    stores = get_stores(request)
    area0 = Area.objects.filter(name__exact=setarea)[0]
    area0.state = True
    area0.save()
    order_by_dic = AllStore.order_by_dic
    store_list = stores
    paginator = Paginator(store_list, 20)
    page = request.GET.get('page')
    try:
        stores_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        stores_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        stores_page = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'areas': areas, 'categories': categories, 'stores_page': stores_page, 'order_by_dic':order_by_dic, 'order_by_get':'star', 'per_consume_min':-1, 'per_consume_max':-1})

def category_index(request, store_id):
    setcategory = Store.objects.filter(id=store_id)[0].category
    areas = Area.objects.all()
    for area in areas:
        area.state = False
        num_t = Store.objects.filter(area__exact=area.name).count()
        area.num = num_t
        area.save()
    categories = Category.objects.all()
    for category in categories:
        category.state = False
        num_t = Store.objects.filter(category__exact=category.name).count()
        category.num = num_t
        category.save()
    stores = get_stores(request)
    category0 = Category.objects.filter(name__exact=setcategory)[0]
    category0.state = True
    category0.save()
    order_by_dic = AllStore.order_by_dic
    store_list = stores
    paginator = Paginator(store_list, 20)
    page = request.GET.get('page')
    try:
        stores_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        stores_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        stores_page = paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'areas': areas, 'categories': categories, 'stores_page': stores_page, 'order_by_dic':order_by_dic, 'order_by_get':'star', 'per_consume_min':-1, 'per_consume_max':-1})
def create(request):
    params = request.POST if request.method == 'POST' else None
    form = StoreForm(params)
    if form.is_valid():
        store = form.save(commit=False)
        store.save()
        messages.info(request, '店铺“{}”添加成功'.format(store.name))
        form = StoreForm()

    return render(request, 'create.html', {'form': form})


def store(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    t = 5
    if (len(store.reviews.all()) < 5):
        t = len(store.reviews.all())
    first_reviews = []
    for i in range(t):
        first_reviews.append(store.reviews.all()[i])
    nearest_stores = Store.objects.filter(category = store.category)
    nearest_stores = nearest_stores.order_by('-star')
    t = 5
    if (len(nearest_stores) < 5):
        t = len(store.reviews.all())
    nearest_store = []
    for i in range(t):
        nearest_store.append(nearest_stores[i + 1])
    return render(request, 'store.html', {'store': store, 'review_form': ReviewForm(), 'first_reviews': first_reviews, 'nearest_stores': nearest_store})

ONE_PAGE_OF_DATA = 10

def review(request, store_id):
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''

    startPos = (curPage - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA
    store = get_object_or_404(Store, pk=store_id)
    reviews = store.reviews.all()[startPos:endPos]
    if curPage == 1 and allPage == 1: #标记1
        allPostCounts = store.reviews.count()
        allPage = allPostCounts // ONE_PAGE_OF_DATA
        remainPost = allPostCounts % ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '全部', 'all': store.reviews.count(),
                                           'sort_path': 'store/{}/review/sort'.format(store_id), 'allPage':allPage, 'curPage':curPage})

global state
state = ''


def review_sort(request, store_id):
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''

    startPos = (curPage - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA

    store = get_object_or_404(Store, pk=store_id)
    reviews = store.reviews.all()
    if 'review-order' in request.POST:
        global state
        state = request.POST['review-order']
    if state == 'latest':
        reviews = reviews.order_by('-create_at')
    elif state == 'oldest':
        reviews = reviews.order_by('create_at')
    elif state == 'likest':
        reviews = reviews.order_by('-like')
    reviews = reviews.all()[startPos:endPos]
    if curPage == 1 and allPage == 1: #标记1
        allPostCounts = store.reviews.count()
        allPage = allPostCounts // ONE_PAGE_OF_DATA
        remainPost = allPostCounts % ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1

    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '全部', 'all': store.reviews.count(),
                                           'sort_path': 'store/{}/review/sort'.format(store_id), 'allPage': allPage,
                                           'curPage': curPage})


def review_star(request, store_id, star):
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''

    startPos = (curPage - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA
    store = get_object_or_404(Store, pk=store_id)
    reviews = Review.objects.filter(star=star, store__id=store.id)[startPos:endPos]
    if curPage == 1 and allPage == 1: #标记1
        allPostCounts = Review.objects.filter(star=star, store__id=store.id).count()
        allPage = allPostCounts // ONE_PAGE_OF_DATA
        remainPost = allPostCounts % ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1
    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '{} 星'.format(star), 'all': Review.objects.filter(star=star, store__id=store.id).count(),
                                           'sort_path': 'store/{}/review/star/{}/sort'.format(store_id, star), 'allPage': allPage, 'curPage': curPage})

global state1
state1 = ''


def review_star_sort(request, store_id, star):
    try:
        curPage = int(request.GET.get('curPage', '1'))
        allPage = int(request.GET.get('allPage', '1'))
        pageType = str(request.GET.get('pageType', ''))
    except ValueError:
        curPage = 1
        allPage = 1
        pageType = ''

    startPos = (curPage - 1) * ONE_PAGE_OF_DATA
    endPos = startPos + ONE_PAGE_OF_DATA

    store = get_object_or_404(Store, pk=store_id)
    reviews = Review.objects.filter(star=star, store__id=store_id)
    if 'review-order' in request.POST:
        global state1
        state1 = request.POST['review-order']
    if state1 == 'latest':
        reviews = reviews.order_by('-create_at')
    elif state1 == 'oldest':
        reviews = reviews.order_by('create_at')
    elif state1 == 'likest':
        reviews = reviews.order_by('-like')
    reviews = reviews.all()[startPos:endPos]
    if curPage == 1 and allPage == 1: #标记1
        allPostCounts = Review.objects.filter(star=star, store__id=store.id).count()
        allPage = allPostCounts // ONE_PAGE_OF_DATA
        remainPost = allPostCounts % ONE_PAGE_OF_DATA
        if remainPost > 0:
            allPage += 1

    return render(request, 'review.html', {'store': store, 'reviews': reviews, 'star': '{} 星'.format(star), 'all': Review.objects.filter(star=star, store__id=store.id).count(),
                                           'sort_path': 'store/{}/review/star/{}/sort'.format(store_id, star), 'allPage': allPage, 'curPage': curPage})


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
def filter_emoji(desstr,restr=''):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)

def add_alldata(request):
    #params = request.POST  if request.method == 'POST' else None
    #form = StoreForm(params)
    in_file = open('mydata3.txt', 'r', encoding = 'utf-8')
    in_string = in_file.read()
    in_string = filter_emoji(in_string)
    shop_id = re.findall(r"s@i#(.+?)#s@i", in_string)
    shop_name = re.findall(r"s@n#(.+?)#s@n", in_string)
    star = re.findall(r"s@s#(.+?)#s@s", in_string)
    phone_number = re.findall(r"p@n#(.+?)#p@n", in_string)
    avg_price = re.findall(r"a@p#(.+?)#a@p", in_string)
    taste = re.findall(r"t@a#(.+?)#t@a", in_string)
    environment = re.findall(r"e@n#(.+?)#e@n", in_string)
    service = re.findall(r"s@e#(.+?)#s@e", in_string)
    review_number = re.findall(r"r@n#(.+?)#r@n", in_string)
    address = re.findall(r"a@d#(.+?)#a@d", in_string)
    opening_time = re.findall(r"o@t#(.+?)#o@t", in_string)
    area = re.findall(r"a@r#(.+?)#a@r", in_string)
    category = re.findall(r"c@a#(.+?)#c@a", in_string)
    n = len(shop_name)
    for i in range(0):
        store = Store()
        store.name = shop_name[i] 
        store.phone_number = phone_number[i]
        store.star = int(star[i])
        store.address = address[i]
        store.review_number = int(review_number[i])
        store.area = area[i]
        store.category = category[i]
        store.perconsume = int(avg_price[i])
        if(len(opening_time[i])>50):
           store.opening_time = "9点到20点"
        else:
           store.opening_time = opening_time[i]
        store.taste_score = float(taste[i])
        store.environment_score = float(environment[i])
        store.service_score = float(service[i])
        store.save()
    stores = Store.objects.all()
    author = re.findall(r"u@n#(.+?)#u@n", in_string)
    star = re.findall(r"t@r#(.+?)#t@r", in_string)
    taste_score = re.findall(r"t@t#(.+?)#t@t", in_string)
    environment_score = re.findall(r"e@t#(.+?)#e@t", in_string)
    service_score = re.findall(r"s@v#(.+?)#s@v", in_string)
    content = re.findall(r"c@x#([\s\S]+?)#c@x", in_string)
    create_at = re.findall(r"c@t#(.+?)#c@t", in_string)
    like = re.findall(r"c@h#(.+?)#c@h", in_string)
    store_id = re.findall(r"c@s#(.+?)#c@s", in_string)
    for i in range(66804):
        print(i)
        review = Review()
        review.author = author[i]
        review.star = int(star[i])
        review.taste_score = int(taste_score[i])
        review.environment_score = 2
        review.service_score = int(service_score[i])
        review.content = content[i]
        review.create_at = '20'+create_at[i][0]+create_at[i][1]+'-'+create_at[i][2]+create_at[i][3]+'-'+create_at[i][4]+create_at[i][5]
        review.like = like[i]
        review.store = Store.objects.filter(id = int(store_id[i]))[0]
        review.save()
    return render(request, 'index.html', {'stores': stores})
    #return render(request, 'create.html', {'form': form})

def delete_alldata(request):
    Store.objects.all().delete();
    Review.objects.all().delete();
    stores = Store.objects.all()
    return render(request, 'index.html', {'stores': stores})
