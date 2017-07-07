
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Store, Review, Idf, StopWord
from .PretreatReview import PretreatReview, is_chinese
import jieba
import math


# 将tfidf向量、idf映射、停用词存入数据库的函数
def add_into_table(pretreat):
    tf_idf_str = ''
    review = 0
    pretreat.calc_tfidf()
    pretreat.calc_vector()
    for review_id in pretreat.tf_idf_vector.keys():
        review = get_object_or_404(Review, pk=review_id)
        tf_idf_str = ''
        for word in pretreat.tf_idf_vector[review_id].keys():
            tf_idf_str += str(word) + ' ' + str(pretreat.tf_idf_vector[review_id][word]) + ' '
        review.tfidf_info = tf_idf_str
        review.save()
    for aword in pretreat.idf_map.keys():
        Idf.objects.create(word=aword, idf=pretreat.idf_map[aword])
    for word in pretreat.stopwords_set:
        StopWord.objects.create(word=word)


def search_paragragh(request):
    return_count = 10

    if 'search_str' in request.POST:
        input_text = request.POST['search_str']

        input_text_length = 0
        input_tf_idf = {}
        # jieba分词
        seg_list = list(jieba.cut(input_text))
        flag = True
        for i in range(len(seg_list)):
            for j in range(len(seg_list[i])):
                if not is_chinese(seg_list[i][j]):
                    flag = False
                    break
            # 不为空串且不含非汉字字符，则为有效词
            if len(seg_list[i]) > 0 and flag:
                input_text_length += 1
                if StopWord.objects.filter(word=seg_list[i]).count() <= 0:
                    if seg_list[i] not in input_tf_idf.keys():
                        input_tf_idf[seg_list[i]] = 1
                    else:
                        input_tf_idf[seg_list[i]] += 1
            flag = True
        for word in input_tf_idf.keys():
            item = Idf.objects.filter(word=word)
            if item.count() > 0:
                idf = item[0].idf
            else:
                idf = 0
            input_tf_idf[word] = input_tf_idf[word] / input_text_length * (
                math.log(Review.objects.count() / (idf + 1)))

        temp_list = []
        for word in input_tf_idf.keys():
            temp_list.append((word, input_tf_idf[word]))
        temp_list.sort(key=lambda x: x[1], reverse=True)
        dimension = min(20, len(temp_list))

        tf_idf_vector = {}
        union_set = set()
        input_set = set()
        review_set = set()
        inner_product_list = []
        i = 0
        for key in input_tf_idf.keys():
            if(i < dimension):
                input_set.add(key)
            i += 1


        # 向量内积
        reviews = Review.objects.all()
        j = 0
        for review in reviews:
            j += 1
            if(j % 1000 == 0):
                print(j)
            review_set.clear()
            union_set.clear()
            tf_idf_vector = {}
            vector_list = review.tfidf_info.split()
            i = 0
            while(i < len(vector_list) - 1):
                tf_idf_vector[vector_list[i]] = float(vector_list[i + 1])
                i += 2
            review_set = set(tf_idf_vector.keys())
            union_set = input_set | review_set
            inner_product = 0
            a_module = b_module = 0
            for word in union_set:
                if word in input_set:
                    a = input_tf_idf[word]
                    a_module += a * a
                else:
                    a = 0
                if word in review_set:
                    b = tf_idf_vector[word]
                    b_module += b * b
                else:
                    b = 0
                inner_product += a * b
            if(a_module == 0 or b_module == 0):
                review.similarity = 0
            else:
                inner_product /= math.sqrt(a_module * b_module)
                review.similarity = inner_product
            review.save()
        reviews = reviews.order_by('-similarity')[:return_count]
        return render(request, 'reviewsearch.html', {'reviews': reviews, 'flag': True})
    return render(request, 'reviewsearch.html', {'reviews': list(), 'flag': False})

