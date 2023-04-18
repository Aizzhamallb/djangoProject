from rest_framework import serializers
from django.db.models import Avg

from .models import Book, BookImages

class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookImages
        exclude = ('id',)


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'author', 'title', 'category', 'preview', 'is_available')

    def to_representation(self, instance):  
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        return repr


class BookDetailSerializer(serializers.ModelSerializer):
    images = BookImageSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'

    def to_representation(self, instance):  
        repr = super().to_representation(instance)
        repr['rating'] = instance.reviews.aggregate(Avg('rating'))['rating__avg']
        repr['reviews_count'] = instance.reviews.count()
        return repr


class BookCreateSerializer(serializers.ModelSerializer):
    images = BookImageSerializer(many=True, read_only=False, required=False)


    class Meta:
        model = Book
        fields = ('author', 'title', 'description', 'category', 'book_file', 'is_available', 'preview', 'images',)

    def create(self, validated_data):
        request = self.context.get('request')
        created_book = Book.objects.create(**validated_data)
        images_data = request.FILES
        images_object = [BookImages(book=created_book, image=image) for image in images_data.getlist('images')]
        BookImages.objects.bulk_create(images_object)
        return created_book
