from django.shortcuts import render
from django.views import View  # Импортируем простую вьюшку
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView

# from django.core.mail import send_mail
# импортируем класс для создание объекта письма с html
from django.core.mail import EmailMultiAlternatives
# импортируем функцию, которая срендерит наш html в текст
from django.template.loader import render_to_string

# Не забываем импортировать нужные функции и пакеты
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
# позволяет выводить данные модели пользователя во view
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
# Импортируем класс, позволяющий удобно осуществлять постраничный вывод
from django.core.paginator import Paginator
from .filters import PostFilter  # импортируем недавно написанный фильтр
from .forms import PostForm
from .models import Post, Category, UserCategory


class NewsList(ListView):
    model = Post                    # указываем модель объекты которой мы будем выводить
    # указываем имя шаблона в котором будет лежать html с инструкциями для представление для пользователя
    template_name = 'news/news.html'
    # указываем имя списка в котором будут лежать все объекты для обращения к списку объектов через html-шаблон
    context_object_name = 'news'
    ordering = ['-time']  # сортировка по цене в порядке убывания
    paginate_by = 10  # поставим постраничный вывод в один элемент
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
    context_object_name = 'post_search'
    ordering = ['-time']  # сортировка по цене в порядке убывания
    # paginate_by = 2  # поставим постраничный вывод в один элемент
    # queryset = Post.objects.order_by('-id')
    # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # вписываем наш фильтр в контекст
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        context['choices'] = Post.TYPE_CHOICES
        context['form'] = PostForm()
        # определение выбора категории и наличия подписки на нее у юзера
        if self.request.GET and self.request.GET['category']:
            user = self.request.user
            # category_selected = Category.objects.get(
            #     id=self.request.GET['category']).category
            category_selected = self.request.GET['category']
            not_subscribed = not UserCategory.objects.filter(
                category=self.request.GET['category'], user=user).exists()
            context['not_subscribed'] = not_subscribed
            context['category_selected'] = category_selected
            print('not_subscribed : ', not_subscribed)
            print('category_selected : ', category_selected)
        return context


# Декоратор для кнопки "Подписаться на категорию" представления PostSearch


# @login_required
def subscribe_me(request):
    user = request.user
    print(dir(request.GET))
    # category_selected = Category.objects.get(
    #     id=request.GET['category']).category
    print('user : ', user)
    print(dir(PostSearch))
    # print('category_selected :', category_selected)

    # subscribe_record = UserCategory(
    #     user=request.user, category=request.GET)
    # subscribe_record.save()

    # category_user = UserCategory.objects.get(
    #     category='category').objects.get(user='user')
    # if not (request.category.filter(category='category').exists() & request.user.filter(user='user').exists()):
    #     category_user.user_set.add(user)
    return redirect('/news/search')


# def subscribe(self, request, *args, **kwargs):
def subscribe(request):
    # берём значения для нового продукта из POST-запроса, отправленного на сервер
    category_selected = request.GET.get('category_selected')
    category_obj = Category.objects.get(id=category_selected)
    # создаём новый продукт и сохраняем
    subscribe = UserCategory(user=request.user, category=category_obj)
    subscribe.save()
    # return super().get(request)
    return redirect('/news/search/?category=' + category_selected)


def unsubscribe(request):
    # берём значения для нового продукта из POST-запроса, отправленного на сервер
    category_selected = request.GET.get('category_selected')
    category_obj = Category.objects.get(id=category_selected)
    # создаём новый продукт и сохраняем
    UserCategory.objects.filter(
        user=request.user, category=category_obj).delete()
    # subscribe.save()
    return redirect('/news/search/?category=' + category_selected)


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post                    # указываем модель объекты которой мы будем выводить
    # указываем имя шаблона в котором будет лежать html с инструкциями для представление для пользователя
    template_name = 'news/post_create.html'
    form_class = PostForm
    # указываем имя списка в котором будут лежать все объекты для обращения к списку объектов через html-шаблон
    context_object_name = 'post_add'
    permission_required = ('news.add_post', )

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # вписываем наш фильтр в контекст
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        context['choices'] = Post.TYPE_CHOICES
        context['form'] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        # создаём новую форму, забиваем в неё данные из POST-запроса
        form = self.form_class(request.POST)
        if form.is_valid():  # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
            fields = form.save()
            print(fields)
            email_query = fields.category.values(
                'subscribers__username', 'subscribers__email')
            print('email_query :', email_query)
            email_list = []
            [email_list.append((i['subscribers__username'],
                               i['subscribers__email'])) for i in email_query]
            print('email_list :', email_list)
            email_set = set(email_list)
            print('email_set:', email_set)
            # и делаем расссылку писем-уведомлений о новом посте всем подписанным пользователям:
            # send_mail(
            #     subject=f"Подписка NewsPaper: {request.POST['tittle']}",
            #     message=f"Здравствуй, username. Новая статья в твоём любимом разделе! {request.POST['text']}",
            #     # здесь указываете почту, с которой будете отправлять (об этом попозже)
            #     from_email='sabanchini@yandex.ru',
            #     # здесь список получателей. Например, секретарь, сам врач и так далее
            #     recipient_list=list(email_set)
            # )
            # пишем цикл перебора значений Username и email множества email_set:
            for i in email_set:
                fields.username = i[0]
                fields.email = i[1]
            # получем наш html
                html_content = render_to_string(
                    'new_post_email.html',
                    {
                        'news': fields,
                    }
                )
                tittle = request.POST['tittle']
                text = request.POST['text']

                # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
                msg = EmailMultiAlternatives(
                    subject=f"Подписка NewsPaper: {fields.tittle}",
                    # это то же, что и message
                    body=f"Здравствуй, {fields.username}. Новая статья в твоём любимом разделе! {fields.text}",
                    from_email='sabanchini@yandex.ru',
                    to=[fields.email],  # это то же, что и recipients_list
                )
                msg.attach_alternative(
                    html_content, "text/html")  # добавляем html
                msg.send()  # отсылаем
        # пароль приложения NewsPaper is: qhshurrwwdduzgdx
        # return super().get(request, *args, **kwargs)
        return redirect('/news')


# дженерик для редактирования объекта
class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.change_post', )

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(
            name='authors').exists()
        return context

# Добавляем функциональное представление для повышения привилегий пользователя до членства в группе premium


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news')

# Неиспользуемая вью (список для подписки на категорию):


class CategoryView(LoginRequiredMixin, View):
    # template_name = 'news/category.html'

    def get(self, request):
        cat_list = Category.objects.all().values('id')
        print(cat_list)
        data = {}
        # data = []
        subscribed = False
        for i in cat_list:
            print(i)
            print(request.user.pk, UserCategory.objects.filter(
                category=i['id']).values('user'))
            subscribed_users = [x['user'] for x in UserCategory.objects.filter(
                category=i['id']).values('user')]
            print(
                f'user = {request.user.pk}, subscribed_users = {subscribed_users}')
            if request.user.pk in subscribed_users:
                subscribed = True
            print(subscribed)
            category_name = Category.objects.get(id=i['id']).category
            data[category_name] = subscribed
            # data.append([category_name, subscribed])
        print(data)
        # print(dir(self))
        return render(request, 'news/category.html', data)


class PostDeleteView(PermissionRequiredMixin, DeleteView):  # дженерик для удаления товара
    template_name = 'news/post_delete.html'
    permission_required = ('news.delete_post', )
    queryset = Post.objects.all()
    # не забываем импортировать функцию reverse_lazy из пакета django.urls
    success_url = reverse_lazy('news:news')


# class Posts(View):

#     def get(self, request):
#         posts = Post.objects.order_by('-time')
#         # Создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы
#         p = Paginator(posts, 1)
#         # Берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу
#         posts = p.get_page(request.GET.get('page', 1))
#         # Теперь вместо всех объектов в списке товаров хранится только нужная нам страница с товарами

#         data = {
#             'news': posts,
#         }
#         print(data)
#         return render(request, 'news/news.html', data)


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'
