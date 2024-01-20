from django.urls import path
from .views import NewsList, PostDetail, PostSearch, PostCreateView, PostUpdateView, PostDeleteView, UserView
from .views import upgrade_me

app_name = 'news'
urlpatterns = [
    path('news/', NewsList.as_view(), name='news'),
    path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('user/', UserView.as_view(), name='user'),
    path('usr/', upgrade_me, name='usr'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
    path('news/add/', PostCreateView.as_view(), name='post_add'),
]
