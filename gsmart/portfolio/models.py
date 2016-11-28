from __future__ import unicode_literals
from django.utils import text
from io import StringIO
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage
from PIL import Image

from django.db import models


class Page(models.Model):
    '''
    Database model for descriptive content of pages on site; allows content to be updated through django admin.
    '''
    subtitle = models.CharField(max_length=50, default="Sub-Title")
    slug = models.SlugField()
    content = models.TextField()

    def save(self, *args, **kwargs):
        self.slug = text.slugify(self.subtitle)
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.subtitle


class Piece(models.Model):
    '''
    Database objects for all piece (artwork) inputs
    '''
    pages = models.ManyToManyField(Page)
    ORIENTATION_CHOICES = (
        ('L', 'Landscape'),
        ('P', 'Portrait'),
        ('O', 'Other')
    )
    orientation = models.CharField(
        max_length=20,
        choices=ORIENTATION_CHOICES,
        default='L'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=False, editable=False)
    height_in = models.IntegerField()
    width_in = models.IntegerField()
    description = models.TextField()
    finish_date = models.DateField()
    created = models.DateField()
    large_image = models.ImageField()
    thumbnail_image = models.ImageField(blank=False, null=False, editable=False)
    small_image = models.ImageField(blank=False, null=False, editable=False)
    draft = models.BooleanField(default=True)
    image_rank = models.IntegerField()
    collage_placement = models.PositiveIntegerField()
    MEDIUM_CHOICES = (
        ('OL', 'Oil'),
        ('PC', 'Pencil'),
        ('IK', 'Ink'),
        ('WC', 'Watercolor'),
        ('DG', 'Digital'),
        ('MM', 'Mixed Media'),
        ('OT', 'Other')
    )
    medium = models.CharField(max_length=50, choices=MEDIUM_CHOICES, default='Oil')

    def save(self, *args, **kwargs):
        """
        Make and save the slugs and the thumbnails here.
        """
        self.slug = self.title.replace(' ', '_').lower()
        super(Piece, self).save(*args, **kwargs)
        #if self.large_image is None or self.small_image is None:
        self.make_thumbnail()

    def __str__(self):
        return self.title

    def make_thumbnail(self):
        """
        Create and save the thumbnail for the photo (simple resize with PIL).
        """
        # open the large_image that was uploaded with PIL Image.open('filepath').

        img_file = storage.open(self.large_image.name, 'r') # convert to file name
        try:
            image = Image.open(img_file.name)
        except FileNotFoundError:
            print('Image not found.')
            return False

        # TODO: do conditional logic for orientation and size to resize images
        height = 300
        conversion_factor = height/image.height
        width = conversion_factor * image.width

        THUMB_SIZE = height, width

        # use PIL .thumbnail(size, resample value) which resizes the image
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS) # use ANTIALIAS to maintain quality of image
        img_file.close()

        # Path to save to, name, and extension
        thumb_name, thumb_extension = os.path.splitext(self.large_image.name)
        thumb_extension = thumb_extension.lower() # converts string to only lowercase chars

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        # validate file types
        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type


        import pdb; pdb.set_trace()

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = StringIO(thumb_filename) # makes a new instance of the StringIO class
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # Load a ContentFile into the thumbnail field so it gets saved
        self.thumbnail_image.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)
        temp_thumb.close()

        return True


class Show(models.Model):
    show_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=200, blank=True, null=False, editable=False)
    show_description = models.TextField()
    show_pieces = models.ManyToManyField(Piece, related_name='shows')
    cover_photo = models.OneToOneField(Piece, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = self.show_title.replace(' ', '_').lower()
        super(Show, self).save(*args, **kwargs)

    def __str__(self):
        return self.show_title


class Post(models.Model):
    '''
    Database objects for any content/blog posts.
    '''
    title = models.CharField(max_length=100, default="Untitled")
    content = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title
