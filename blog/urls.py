from django.urls import path
from blog.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path("about/",about,name='about'),
    path('contact/', contact, name='contact'),
    path("login/",login_page,name='login'),
    path("logout",logout_view,name='logout'),
    path("register/",register,name='register'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path("profile/<str:username>/edit/", edit_profile, name="edit_profile"),
    path('', post_list, name='post_list'),
    path('posts/new/', post_create, name='post_create'),
    path('posts/<int:pk>/', post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', update_post, name='update_post'),
    path('posts/<int:pk>/delete/', delete_post, name='delete_post'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/like/', like_comment, name='like_comment'),
    path('comment/<int:comment_id>/dislike/', dislike_comment, name='dislike_comment'),
    path('tag/<str:tag_name>/', posts_by_tag, name='posts_by_tag'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)