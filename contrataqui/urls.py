from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("site_final.urls")),
    path("usuarios/", include("django.contrib.auth.urls")),
    path("usuarios/", include("usuarios_site.urls")),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
