from django.contrib import admin
from .models import  Page, Piece, Post, Show
# Register your models here.
admin.site.register(Piece)
admin.site.register(Post)
admin.site.register(Page)
admin.site.register(Show)
