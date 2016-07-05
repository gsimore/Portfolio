from django.shortcuts import render
from django.http import HttpResponse
from .models import Piece
# Create your views here.

def home(request):
    pieces = Piece.objects.order_by('image_rank')
    return render(request, 'gallery.html', {'pieces':pieces})

def piece_detail(request, title):
    piece = Piece.objects.get(title=title)
    return render(request, 'piece_detail.html', {'piece':piece})
