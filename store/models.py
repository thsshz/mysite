from django.db import models
from django.utils import timezone

# Create your models here.


class Store(models.Model):
    name = models.CharField(max_length=50, verbose_name="店名")
    phone_number = models.CharField(max_length=50, verbose_name="电话")
    address = models.TextField(verbose_name="地址")
    review_number = models.IntegerField(verbose_name="评论数")


class Review(models.Model):
    # id = models.IntegerField()
    author = models.CharField(max_length=50, verbose_name="客户")
    star = models.IntegerField(verbose_name="总体评价")
    taste_score = models.IntegerField(verbose_name="口味")
    environment_score = models.IntegerField(verbose_name="环境")
    service_score = models.IntegerField(verbose_name="服务")
    content = models.TextField(verbose_name="评价内容")
    store = models.ForeignKey('Store', related_name='reviews', related_query_name='review')
    create_at = models.DateTimeField(default=timezone.now)
    like = models.IntegerField(verbose_name="点赞数")
