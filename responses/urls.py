from django.urls import path
from .views import ResponseCreateView, ResponseListView, delete_response, accept_response

urlpatterns = [
    path('responses/add/<int:post_id>/', ResponseCreateView.as_view(), name='add_response'),
    path('responses/', ResponseListView.as_view(), name='response_list'),
    path('responses/delete/<int:pk>/', delete_response, name='delete_response'),
    path('responses/accept/<int:pk>/', accept_response, name='accept_response'),
]
