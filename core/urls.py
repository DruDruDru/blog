from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView

from . import views

urlpatterns = [
    # Представления постов и комментариев
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/create/', views.PostCreationView.as_view(), name='post_create'),
    path('posts/<int:pk>/comment/create/', views.CommentCreationView.as_view(), name='comment_create'),
    path('posts/<int:post_pk>/comment/delete/<int:pk>', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('posts/<int:post_pk>/comment/update/<int:pk>', views.CommentChangeView.as_view(), name='comment_update'),

    # Представления пользователя и его профиля
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/sighup/', views.UserCreationView.as_view(), name='sighup'),
    path('accounts/profile/<slug:pk>', views.UserDetailView.as_view(), name='user_detail'),
    path('accounts/profile/update/<slug:pk>', views.UserChangeView.as_view(), name='user_update'),
    path('accounts/profile/delete/<slug:pk>', views.UserDeleteView.as_view(), name='user_delete'),
]
