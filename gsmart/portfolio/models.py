from __future__ import unicode_literals
from django.utils import text

from django.db import models


def singleton(class_):
  instances = {}
  def getinstance(*args, **kwargs):
    if class_ not in instances:
        instances[class_] = class_(*args, **kwargs)
    return instances[class_]
  return getinstance


class GlobalAttribute(models.Model):
    title = models.CharField(max_length=50, default="Website Title")

    def __str__(self):
        return self.title


class Page(models.Model):
    website = models.ForeignKey(GlobalAttribute)
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
    ORIENTATION_CHOICES = (('L', 'Landscape'), ('P', 'Portrait'), ('O', 'Other'))
    orientation = models.CharField(max_length=20, choices=ORIENTATION_CHOICES, default='L')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=False, editable=False)
    height_in = models.IntegerField()
    width_in = models.IntegerField()
    description = models.TextField()
    finish_date = models.DateField()
    created = models.DateField()
    thumbnail_image = models.ImageField()
    small_image = models.ImageField()
    large_image = models.ImageField()
    draft = models.BooleanField(default=True)
    image_rank = models.IntegerField()
    collage_placement = models.PositiveIntegerField()
    medium = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        self.slug = self.title.replace(' ', '_').lower()
        super(Piece, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Post(models.Model):
    title = models.CharField(max_length=100, default="Untitled")
    content = models.TextField()
    date_created = models.DateTimeField(auto_now = True)
    published = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title

@singleton
class About(Post):
    additional = models.TextField(blank=True, null=True)
