from django.db import models
from django.utils import timezone

# Create your models here.


class Store(models.Model):
    # id = models.IntegerField()
    name = models.CharField(max_length=50, verbose_name="店名")
    phone_number = models.CharField(max_length=50, verbose_name="电话")
    star = models.IntegerField(verbose_name="星级", default = 0)
    address = models.TextField(verbose_name="地址", default = '')
    review_number = models.IntegerField(verbose_name="评论数")
    area = models.CharField(max_length=50, verbose_name="区域", default = '')
    category = models.CharField(max_length=50, verbose_name="类别", default = '')
    per_consume = models.IntegerField(verbose_name="人均消费", default = 0)
    opening_time = models.CharField(max_length=50, verbose_name="营业时间", default = '')
    taste_score = models.FloatField(verbose_name="口味", default = 0.0)
    environment_score = models.FloatField(verbose_name="环境", default = 0.0)
    service_score = models.FloatField(verbose_name="服务", default = 0.0)

class Review(models.Model):
    # id = models.IntegerField()
    author = models.CharField(max_length=50, verbose_name="客户")
    star = models.IntegerField(verbose_name="总体评价")
    taste_score = models.IntegerField(verbose_name="口味")
    environment_score = models.IntegerField(verbose_name="环境")
    service_score = models.IntegerField(verbose_name="服务")
    content = models.TextField(verbose_name="评价内容")
    store = models.ForeignKey('Store', related_name='reviews', related_query_name='review')
    create_at = models.DateField(default=timezone.now)
    like = models.IntegerField(verbose_name="点赞数")

class Area(models.Model):
    # id = models.IntegerField()
    name = models.CharField(max_length=50, verbose_name="区域名")
    state = models.BooleanField(verbose_name="状态", default=False)
    num = models.BigIntegerField(verbose_name="数量", default = 0)

class Category(models.Model):
    # id = models.IntegerField()
    name = models.CharField(max_length=50, verbose_name="类型名")
    state = models.BooleanField(verbose_name="状态", default=False)
    num = models.BigIntegerField(verbose_name="数量", default = 0)
