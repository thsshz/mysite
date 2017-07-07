import jieba
import math


def is_chinese(uchar):
    if '\u4e00' <= uchar <= '\u9fa5':
        return True
    else:
        return False


class PretreatReview:
    def __init__(self):
        self.idf_map = {}
        self.tf_idf_map = {}
        self.length_map = {}
        self.review_count = 0
        self.stopwords_set = set()
        self.tf_idf_vector = {}
        self.tf_idf_vector_dimension = 20
        self.return_num = 100

        # 读取停用词词表
        file = open('百度停用词列表.txt', 'r', encoding='UTF-8')
        while 1:
            line = file.readline()
            line = line.strip('\n')
            if not line:
                break
            self.stopwords_set.add(line)

    def process_text(self, review, review_id):
        if len(review) == 0:
            return
        self.review_count += 1
        # jieba分词
        seg_list = list(jieba.cut(review))
        # print(seg_list)
        flag = True
        self.length_map[review_id] = 0
        self.tf_idf_map[review_id] = {}
        for i in range(len(seg_list)):
            for j in range(len(seg_list[i])):
                if not is_chinese(seg_list[i][j]):
                    flag = False
                    break
            # 不为空串且不含非汉字字符，则为有效词
            if len(seg_list[i]) > 0 and flag:
                if seg_list[i] not in self.stopwords_set:
                    if seg_list[i] not in self.tf_idf_map[review_id].keys():
                        self.tf_idf_map[review_id][seg_list[i]] = 1
                    else:
                        self.tf_idf_map[review_id][seg_list[i]] += 1
                    if seg_list[i] not in self.idf_map.keys():
                        self.idf_map[seg_list[i]] = 1
                    elif self.tf_idf_map[review_id][seg_list[i]] == 1:
                        self.idf_map[seg_list[i]] += 1
                self.length_map[review_id] += 1
            flag = True

    def calc_tfidf(self):
        for key in self.tf_idf_map.keys():
            for key_in in self.tf_idf_map[key].keys():
                self.tf_idf_map[key][key_in] = self.tf_idf_map[key][key_in] / self.length_map[key] * (
                    math.log(self.review_count / (self.idf_map[key_in] + 1)))

    def calc_vector(self):
        temp_list = []
        for review_id in self.tf_idf_map.keys():
            self.tf_idf_vector[review_id] = {}
            temp_list.clear()
            for word in self.tf_idf_map[review_id].keys():
                temp_list.append((word, self.tf_idf_map[review_id][word]))
            temp_list.sort(key=lambda x: x[1], reverse=True)
            dimension = min(self.tf_idf_vector_dimension, len(temp_list))
            for i in range(dimension):
                self.tf_idf_vector[review_id][temp_list[i][0]] = temp_list[i][1]

    def search_comment(self, input_text):
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
                if seg_list[i] not in self.stopwords_set:
                    if seg_list[i] not in input_tf_idf.keys():
                        input_tf_idf[seg_list[i]] = 1
                    else:
                        input_tf_idf[seg_list[i]] += 1
            flag = True
        for word in input_tf_idf.keys():
            if word in self.idf_map.keys():
                idf = self.idf_map[word]
            else:
                idf = 0
            print(idf)
            print(self.review_count)
            input_tf_idf[word] = input_tf_idf[word] / input_text_length * (
                                 math.log(self.review_count / (idf + 1)))

        temp_list = []
        input_tf_idf_vector = []
        for word in input_tf_idf.keys():
            temp_list.append((word, input_tf_idf[word]))
        temp_list.sort(key=lambda x: x[1], reverse=True)
        dimension = min(self.tf_idf_vector_dimension, len(temp_list))
        for i in range(dimension):
            input_tf_idf_vector.append(temp_list[i])

        union_set = set()
        input_set = set()
        review_set = set()
        inner_product_list = []

        for item in input_tf_idf_vector:
            input_set.add(item[0])
        # 向量内积

        for review_id in self.tf_idf_vector.keys():
            review_set.clear()
            union_set.clear()
            for word in self.tf_idf_vector[review_id].keys():
                review_set.add(word)
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
                    b = self.tf_idf_vector[review_id][word]
                    b_module += b * b
                else:
                    b = 0
                inner_product += a * b
            if(a_module == 0 or b_module == 0):
                inner_product = 0
            else:
                inner_product /= math.sqrt(a_module * b_module)
            inner_product_list.append((review_id, inner_product))

        inner_product_list.sort(key=lambda x: x[1], reverse=True)
        return inner_product_list[:self.return_num]

