# serializers.py
from rest_framework import serializers
from .models import News, NewsMedia

class NewsMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsMedia
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    media = NewsMediaSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = '__all__'