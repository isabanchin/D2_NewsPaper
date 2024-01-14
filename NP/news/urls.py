from django.urls import path
from .views import NewsList, PostDetail, Posts, PostSearch

app_name = 'news'
urlpatterns = [
    path('news/', NewsList.as_view()),
    path('news/<int:pk>/', PostDetail.as_view()),
    # Не забываем добавить эндпойнт для нового класса-представления%
    path('posts/', Posts.as_view(),),
    path('news/search/', PostSearch.as_view(),),
]
