from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from project_app.views import DashbroadView, supply_lists

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashbroad/', DashbroadView.as_view()),
    path('supply_lists/', supply_lists)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
