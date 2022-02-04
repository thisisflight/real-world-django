import debug_toolbar
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('api/events/', include('events.urls_api')),
    path('mail/', include('mail.urls')),
    # API
    path('api/mail/', include('mail.urls_api')),
    # other
    path('__debug__/', include(debug_toolbar.urls))
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
