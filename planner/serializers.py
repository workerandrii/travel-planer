from rest_framework import serializers
from .models import Place

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'project', 'external_id', 'notes', 'is_visited']
        read_only_fields = ['project']