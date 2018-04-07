from django.conf.urls import include, path

# from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    
    path('search/', include('haystack.urls')),
    path('admin/', admin.site.urls),
    path('s/', include('search_ui.urls')),
]

# urlpatterns = [

# 	url(r'^search/', include('haystack.urls')),
# ]