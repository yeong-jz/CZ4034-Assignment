from django.conf.urls import include, path

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    
    path('search/', include('haystack.urls')),
    path('admin/', admin.site.urls),
    path('s/', include('search_ui.urls')),
]
