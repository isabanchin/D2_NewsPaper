from django.urls import path
from .views import NewsList, PostDetail, PostSearch, PostCreateView, PostUpdateView, PostDeleteView, UserView, CategoryView
from .views import upgrade_me, subscribe, unsubscribe
from django.views.decorators.cache import cache_page  # модуль кэширования

app_name = 'news'
urlpatterns = [
    # добавим кеширование 1 минута для главной страницы носостей:
    path('news/', cache_page(60*1)(NewsList.as_view()), name='news'),
    # добавим кэширование 5 минут для страницы поста:
    path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('news/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('user/', UserView.as_view(), name='user'),
    path('usr/', upgrade_me, name='usr'),
    path('news/subscribe/', subscribe, name='subscribe'),
    path('news/unsubscribe/', unsubscribe, name='unsubscribe'),
    path('news/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
    path('news/add/', PostCreateView.as_view(), name='post_add'),
    path('news/cat/', CategoryView.as_view(), name='category'),
]
