from django.contrib import admin
from .models import Activity, Article, Book, Grade, ReadingGroup, ReadingGroupMembership, Note, UserProfile

admin.site.register([Activity, Article, Book, Grade, ReadingGroup, ReadingGroupMembership, Note, UserProfile])
