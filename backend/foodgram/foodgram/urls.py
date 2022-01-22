from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('recipes.urls')),
    path('api/ingredients/', include('ingredients.urls')),
    path('api/tags/', include('tags.urls')),
]
