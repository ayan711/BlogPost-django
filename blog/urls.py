
from django.contrib import admin
from django.urls import path
from .views import home,about,PostListView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView

urlpatterns = [
    # as_view() is used to convert class based views to use as argument in url_patterns
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    # Function based view for listing views
    # path('', home,name='blog-home'),
    path('about/',about,name='blog-about'),
    # DetailView takes an id as param to get details of the record....by default it expect variable pk to load the data
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
]
