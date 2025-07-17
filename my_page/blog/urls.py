from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('posts', views.show_all_post, name='all_posts'),
    path('posts/user', views.search_by_user, name='search_by_user'),
    path('posts/delete', views.delete_post_by_id, name='delete_posts'),
    path('posts/update', views.update_post_by_id, name='update_posts'),
]
