from django.shortcuts import render
from django.http import HttpResponse
from .models import Piece
# Create your views here.


def home(request):
    pieces = Piece.objects.order_by('image_rank')

    return render(request, 'gallery.html', {'pieces':pieces})


def piece_detail(request, slug):
    piece = Piece.objects.get(slug=slug)
    slugs = [i.slug for i in Piece.objects.order_by('image_rank')]
    current_index = slugs.index(piece.slug)

    if current_index == len(slugs)-1:
        next_slug = slugs[0]
    else:
        next_slug = slugs[current_index+1]
    #import pdb; pdb.set_trace()
    previous_slug = slugs[current_index-1]

    return render(request, 'piece_detail.html', locals())
