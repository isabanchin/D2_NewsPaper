from django.shortcuts import render
from django.views import View  # Импортируем простую вьюшку

# позволяет выводить данные модели пользователя во view
from django.views.generic import ListView, DetailView
# Импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.core.paginator import Paginator
from .filters import PostFilter  # импортируем недавно написанный фильтр
from .models import Post, Category


class NewsList(ListView):
    model = Post                    # указываем модель объекты которой мы будем выводить
    # указываем имя шаблона в котором будет лежать html с инструкциями для представление для пользователя
    template_name = 'news/news.html'
    # указываем имя списка в котором будут лежать все объекты для обращения к списку объектов через html-шаблон
    context_object_name = 'news'
    ordering = ['-id']  # сортировка по цене в порядке убывания
    paginate_by = 1  # поставим постраничный вывод в один элемент
    # queryset = Post.objects.order_by('-id')
    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # вписываем наш фильтр в контекст
    #     context['filter'] = PostFilter(
    #         self.request.GET, queryset=self.get_queryset())
    #     return context


class PostSearch(ListView):
    model = Post                    # указываем модель объекты которой мы будем выводить
    # указываем имя шаблона в котором будет лежать html с инструкциями для представление для пользователя
    template_name = 'news/search.html'
    # указываем имя списка в котором будут лежать все объекты для обращения к списку объектов через html-шаблон
    context_object_name = 'postsearch'
    ordering = ['-id']  # сортировка по цене в порядке убывания
    paginate_by = 2  # поставим постраничный вывод в один элемент
    # queryset = Post.objects.order_by('-id')
    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # вписываем наш фильтр в контекст
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class Posts(View):

    def get(self, request):
        posts = Post.objects.order_by('-time')
        # Создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы
        p = Paginator(posts, 1)
        # Берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу
        posts = p.get_page(request.GET.get('page', 1))
        # Теперь вместо всех объектов в списке товаров хранится только нужная нам страница с товарами

        data = {
            'news': posts,
        }
        print(data)
        return render(request, 'news/news.html', data)


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'
