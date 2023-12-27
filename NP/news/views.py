# from django.shortcuts import render

# позволяет выводить данные модели пользователя во view
from django.views.generic import ListView, DetailView
from .models import Post, Category


class NewsList(ListView):
    model = Post                    # указываем модель объекты которой мы будем выводить
    # указываем имя шаблона в котором будет лежать html с инструкциями для представление для пользователя
    template_name = 'news/news.html'
    # указываем имя списка в котором будут лежать все объекты для обращения к списку объектов через html-шаблон
    context_object_name = 'news'
    queryset = Post.objects.order_by('-id')


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'
