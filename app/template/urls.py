from django.urls import path
from .views import BaseView
from template.constant import PAGE_ROUTE
from django.conf.urls.static import static
from django.conf import settings

url_paths = PAGE_ROUTE
url: list = []
urlpatterns: list = []


for url_path in url_paths:
    url.append(path(url_path.get("route"), BaseView.index, name=url_path.get("name")))

urlpatterns = url + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
