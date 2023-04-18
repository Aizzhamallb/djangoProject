from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    slug = models.SlugField(max_length=70, primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', blank=True, null=True)

    def __str__(self):
        return f'{self.slug} --> {self.parent}' if self.parent else self.slug
    

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'