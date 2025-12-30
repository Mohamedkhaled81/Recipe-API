"""
Tags View
"""

from rest_framework import viewsets
from core.models import Tag
from .serializers import TagSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class TagModelViewSet(viewsets.ModelViewSet):
    """Tags actions"""

    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = TagSerializer

    def get_queryset(self):
        """Retrieve Tags created by auth user"""
        return self.queryset.filter(user=self.request.user).order_by("-name")

    def perform_create(self, serializer):
        """adding user when creating tag"""
        serializer.save(user=self.request.user)
