from django.contrib import admin
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Generates the schema
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    # Serve the swagger documentation for making GUI for our doc
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs'
        )
]
