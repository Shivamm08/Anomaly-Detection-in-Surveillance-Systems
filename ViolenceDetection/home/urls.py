from django.urls import path,include
from home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.index, name="home"),
    path("upload/", views.upload, name="upload"),
    path("realtime/", views.realtime, name="realtime"),
    path("base/", views.base, name="base"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)