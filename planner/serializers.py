from rest_framework import serializers
from .models import Place, Project

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'project', 'external_id', 'notes', 'is_visited']
        read_only_fields = ['project']

class ProjectSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'is_completed', 'places']
        read_only_fields = ['is_completed']


    def create(self, validated_data):
        """
        Saves the project and its bulk-imported places securely in one go.
        """
        places_data = validated_data.pop('places', [])
        project = Project.objects.create(**validated_data)
        
        for place_data in places_data:
            Place.objects.create(project=project, **place_data)
            
        return project