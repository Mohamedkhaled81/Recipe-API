from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter
from tag import views

app_name = 'tag'

router = DefaultRouter()
router.register('', views.TagModelViewSet)

urlpatterns = router.urls