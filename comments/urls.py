from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('<int:post_id>/', views.post_comments, name='comments'),
    path('my/', views.user_comments, name='user_comments'),
]
