from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Piece
from portfolio.forms import ContactForm
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from django.contrib import messages
# Create your views here.

def home(request):

    return render(request, 'home.html')


def contact(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)
        
        if not form.is_valid():
            message = "Invalid Form!!!"
            return render(request, 'contact.html', {'form': form_class, 'message':messages})


        elif form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )

            email.send()
            messages.add_message(request, messages.INFO, 'Your message was submitted!')
            return render(request, 'contact.html', {'form': form_class, 'message':messages})

    return render(request, 'contact.html', {'form': form_class})


def gallery(request):
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
