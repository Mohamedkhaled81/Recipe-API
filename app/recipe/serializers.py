"""
Recipe Serializers
"""
from rest_framework import serializers
from core.models import Recipe, Tag
from tag.serializers import TagSerializer

class RecipeReadSerializer(serializers.ModelSerializer):
    """Recipe Read Serializer"""
    tags = TagSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

class RecipeReadDetailsSerializer(RecipeReadSerializer):
    """Serializer for recipe detail view."""
    class Meta(RecipeReadSerializer.Meta):
        fields = RecipeReadSerializer.Meta.fields + ["description"]

class RecipeWriteSerializer(serializers.ModelSerializer):
    """Recipe Write Serializer"""
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False,
        )
        
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags', 'description']
        read_only_fields = ['id']
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["tags"] = TagSerializer(instance.tags.all(), many=True).data
        return data





