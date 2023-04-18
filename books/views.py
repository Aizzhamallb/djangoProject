from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from rating.serializers import ReviewSerializer
from . import serializers
from .models import Book


class StandartResultPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    max_page_size = 100


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter,)
    filterset_fields = ('category', 'author',)
    search_fields = ('title', 'author')
    pagination_class = StandartResultPagination


    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.BookListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
            return serializers.BookCreateSerializer
        return serializers.BookDetailSerializer


    def get_permissions(self):
        
        if self.action in ('create', 'update', 'partial_update', 'destroy',):
            return (permissions.IsAdminUser(),)
        
        else:
            return [permissions.AllowAny()]


    # api/v1/books/<id>/reviews/
    @action(['GET', 'POST'], detail=True)
    def reviews(self, request, pk=None):
        book = self.get_object()
        if request.method == 'GET':
            reviews = book.reviews.all()
            serializer = ReviewSerializer(reviews, many=True).data
            return Response(serializer, status=200)
        data = request.data
        serializer = ReviewSerializer(data=data, context={'request': request, 'book': book})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)


