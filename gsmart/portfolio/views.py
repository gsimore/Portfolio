from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from portfolio.forms import ContactForm
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context
from django.contrib import messages
from .models import Piece, Post, Show, Page


def home(request):
    """
    TODO: WRITE BETTER DOC STRINGS
    """
    shows = Show.objects.order_by('-id')  # TODO: another ordering criteria.
    page = Page.objects.get(slug="home")

    #import pdb; pdb.set_trace()
    context = {'shows': shows, 'page': page}
    return render(request, 'home.html', context)


def contact(request):
    page = Page.objects.get(slug="contact")
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if not form.is_valid():
            message = "Invalid Form!!!"
            return render(request, 'contact.html', {'form': form_class, 'message':messages})


        elif form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
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
                "Your website" + '',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email}
            )

            email.send()
            messages.add_message(request, messages.INFO, 'Your message was submitted!')
            return render(request, 'contact.html', {'form':form_class, 'message': messages, 'page': page})

    return render(request, 'contact.html', {'form':form_class, 'page': page})


def about(request):
    page = Page.objects.get(slug="about")

    return render(request, 'about.html', {'page': page})


def gallery(request, slug):
    page = Page.objects.get(slug="gallery")
    show = Show.objects.get(slug=slug)

    return render(request, 'gallery.html', locals())


def piece_detail(request, slug):
    page = Page.objects.get(slug="art")
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
