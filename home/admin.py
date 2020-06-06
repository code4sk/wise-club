from django.contrib import admin
from book.models import *
from user.models import *

admin.site.register(Book)
admin.site.register(Genre)
# admin.site.register(Author)
admin.site.register(CustomUser)
admin.site.register(Comment)
