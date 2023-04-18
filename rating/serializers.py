from rest_framework import serializers

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    book = serializers.ReadOnlyField(source='book.title')
    
    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        book = self.context.get('book')
        validated_data['user'] = user
        validated_data['book'] = book
        return super().create(validated_data)

    