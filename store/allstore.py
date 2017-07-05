
from django.shortcuts import render
from .models import Store, Area, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class AllStore:
    #order = '星级'
    #per_consume_min = -1
    #per_consume_max = -1
    order_by_dic = {'星级':'star', '评论数':'review_number', '人均消费':'per_consume', '口味':'taste_score', '环境':'environment_score', '服务':'service_score'}

def get_stores(request):
    stores = Store.objects.none()
    flag = 0
    areas = Area.objects.all()
    for area in areas:
        if area.state:
            stores = stores | Store.objects.filter(area__exact=area.name)
            flag = 1
    if flag == 0:
        stores = Store.objects.all()
    flag = 0
    stores2 = Store.objects.none()
    categories = Category.objects.all()
    for category in categories:
        if category.state:
            stores2 = stores2 | stores.filter(category__exact=category.name)
            flag = 1
    if flag == 0:
        stores2 = stores
    return stores2

def filter(request):
    areas = Area.objects.all()
    for area in areas:
        if request.POST.get(area.name):      
            area.state = True
        else:
            area.state = False
        area.save()
    categories = Category.objects.all()
    for category in categories:
        if request.POST.get(category.name):  
            category.state = True
        else:
            category.state = False
        category.save()  
    stores = get_stores(request)
    if request.POST.get('per_consume_min'):
        per_consume_min = request.POST.get('per_consume_min')
        stores = stores.filter(per_consume__gte=per_consume_min)
    else:
        per_consume_min = -1
    if request.POST.get('per_consume_max'):
        per_consume_max = request.POST.get('per_consume_max')
        stores = stores.filter(per_consume__lte=per_consume_max)
    else:
        per_consume_max = -1
    for area in areas:
        num_t = stores.filter(area__exact=area.name).count()
        area.num = num_t
        area.save()
    categories = Category.objects.all()
    for category in categories:
        num_t = stores.filter(category__exact=category.name).count()
        category.num = num_t
        category.save()
    if request.POST.get('order_by'):
        order_by_get = request.POST.get('order_by')
        AllStore.order = order_by_get
        order_use = '-' + order_by_get
        stores = stores.order_by(order_use)
    else:
        order_by_get = AllStore.order
        order_use = '-' + order_by_get
        stores = stores.order_by(order_use)
   
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
    return render(request, 'index.html', {'areas': areas, 'categories': categories, 'stores_page': stores_page, 'order_by_dic':order_by_dic, 'order_by_get':order_by_get, 'per_consume_min':per_consume_min, 'per_consume_max':per_consume_max})
