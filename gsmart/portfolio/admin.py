from django.contrib import admin
from .models import  GlobalAttribute, Page, Piece, Post
# Register your models here.
admin.site.register(Piece)
admin.site.register(Post)
admin.site.register(Page)
admin.site.register(GlobalAttribute)
