from django.urls import path
from .views import HomePageView, PostListView, PostCreateView, PostUpdateView, PostDeleteView, CategoryPostsView, PostDetailView

urlpatterns = [
    path('home', HomePageView.as_view(), name='home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('list/', PostListView.as_view(), name='post_list'),
    path('category/<int:pk>/', CategoryPostsView.as_view(), name='category_posts'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('update/<int:pk>/', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
]

