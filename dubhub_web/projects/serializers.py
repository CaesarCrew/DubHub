from rest_framework import serializers
from .models import Projects

class ProjectsSerializer(serializers.ModelSerializer):
    director_email = serializers.EmailField(source='director.email', read_only=True)

    class Meta:
        model = Projects
        fields = [
            'id',
            'title',
            'description',
            'created_at',
            'foto',
            'director',
            'director_email',
        ]
        read_only_fields = ['id', 'created_at']