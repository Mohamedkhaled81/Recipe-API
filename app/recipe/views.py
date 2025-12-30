"""
Views for Recipe CRUD operations..
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""

    # We added RecipeDetailsSerializer as the default serializer
    # Because we are going to need it for ather actions like Update - Create
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeReadDetailsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve reciepes for auth users."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action in ["create", "update", "destroy", "partial_update"]:
            return serializers.RecipeWriteSerializer
        elif self.action == "list":
            return serializers.RecipeReadSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        # Validated serializer
        serializer.save(user=self.request.user)
