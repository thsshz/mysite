from django.contrib import admin

from .models import Store, Review, Area, Category, Photo, Client, Idf, StopWord

admin.site.register(Store)
admin.site.register(Review)
admin.site.register(Area)
admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(Client)
admin.site.register(Idf)
admin.site.register(StopWord)

# Register your models here.
