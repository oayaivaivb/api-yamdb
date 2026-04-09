from rest_framework import serializers
from .models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

    def validate_score(self, value):
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
