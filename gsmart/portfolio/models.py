from __future__ import unicode_literals

from django.db import models

class Piece(models.Model):
    '''
    Database objects for all piece (artwork) inputs
    '''
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
