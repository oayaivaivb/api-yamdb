from rest_framework import serializers
from .models import Review, Comment

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.IntegerField(read_only=True)
    title = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.IntegerField(read_only=True)
    review = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
