from django.shortcuts import render
from .models import Store, Review,Area, Category
from .reviewsearch import add_into_table
from .PretreatReview import PretreatReview
import re

pretreat  = PretreatReview()

def filter_emoji(desstr,restr=''):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)

def add_alldata(request):
    #params = request.POST  if request.method == 'POST' else None
    #form = StoreForm(params)
    #in_file = open('mydata3.txt', 'r', encoding = 'utf-8')
    in_string = ''
    #in_string = in_file.read()
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
    for i in range(0):
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
    #pretreat = PretreatReview()
    for i in range(10000):
        review = Review.objects.all()[i]
        pretreat.process_text(review.content, review.id)
        print(i)
    #add_into_table(pretreat)
    pretreat.calc_tfidf()
    pretreat.calc_vector()
    return render(request, 'index.html', {'stores': stores})

def delete_alldata(request):
    Store.objects.all().delete();
    Review.objects.all().delete();
    stores = Store.objects.all()
    return render(request, 'index.html', {'stores': stores})

def search_paragragh(request):
    if('search_str' in request.POST):
        input_text = request.POST['search_str']
        result_list = pretreat.search_comment(input_text)
        return render(request, 'reviewsearch.html', {'reviews': result_list})
    return render(request, 'reviewsearch.html', {'reviews': list()})
