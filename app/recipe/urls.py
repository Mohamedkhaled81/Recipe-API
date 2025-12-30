"""
URL mapping for the recipe app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from recipe import views

# This is for calling the reverse method
app_name = "recipe"

router = DefaultRouter()
router.register("", views.RecipeViewSet)

# including the urls that are created by the routers..
urlpatterns = router.urls
