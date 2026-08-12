from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_list, name='report'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('create/post/<int:post_id>/', views.create_report_view, name='create_report'),
]
