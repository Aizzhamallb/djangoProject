from django.db import models
from category.models import Category


class Book(models.Model):
    '''
    Available books
    '''
    author = models.CharField(max_length=150)
    title = models.CharField(max_length=250)
    description = models.TextField()
    book_file = models.FileField(upload_to='files/')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, related_name='books', on_delete=models.CASCADE)
    preview = models.ImageField(upload_to='images/', null=True)    

    def __str__(self):
        return f'{self.author} -- {self.title}'

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
    

class BookImages(models.Model):
    image = models.ImageField(upload_to='images/')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='images')
   