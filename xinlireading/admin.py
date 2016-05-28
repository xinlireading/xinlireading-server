from django.contrib import admin
# from .models import Question
from .models import Activity, Article, Book, Grade, ReadingGroup, ReadingGroupMembership, Note, Person, PersonFavoriteBook
# Register your models here.
# admin.site.register(Question)
admin.site.register([Activity, Article, Book, Grade, ReadingGroup, ReadingGroupMembership, Note, Person, PersonFavoriteBook])
