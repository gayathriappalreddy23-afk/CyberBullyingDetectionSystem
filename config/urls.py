from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
<<<<<<< HEAD
    path("admin/", admin.site.urls),

    path("", include("home.urls")),
    path("accounts/", include("accounts.urls")),
    path("prediction/", include("prediction.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("posts/", include("posts.urls")),
    path("reports/", include("reports.urls")),
=======
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('prediction/', include('prediction.urls', namespace='prediction')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('comments/', include('comments.urls', namespace='comments')),
    path('reports/', include('reports.urls', namespace='reports')),
>>>>>>> 6992ec5fd9a63d60a45e1acd7df7d8e8e9678870
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )