from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('prediction/', include('prediction.urls', namespace='prediction')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('comments/', include('comments.urls', namespace='comments')),
    path('reports/', include('reports.urls', namespace='reports')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )