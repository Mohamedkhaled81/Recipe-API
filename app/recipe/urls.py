"""
URL mapping for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)

# This is for calling the reverse method
app_name = 'recipe'

# including the urls that are created by the routers..
urlpatterns = [
    path('', include(router.urls))
]
