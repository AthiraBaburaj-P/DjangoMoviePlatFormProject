from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Profile, Movie, Review, Category

admin.site.register(Profile)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(Category)
