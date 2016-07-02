from __future__ import unicode_literals

from django.db import models

class Piece(models.Model):
    title = models.CharField(max_length=200)
    height_in = models.IntegerField()
    width_in = models.IntegerField()
    description = models.TextField()
    finish_date = models.DateTimeField()
    created = models.DateTimeField()
    small_image = models.ImageField()
    large_image = models.ImageField()
    draft = models.BooleanField(default=True)
