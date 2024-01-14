# импортируем filterset, чем-то напоминающий знакомые дженерики
from django_filters import FilterSet
from django_filters import ModelChoiceFilter
from .models import Post, Author


# создаём фильтр
class PostFilter(FilterSet):
    author = ModelChoiceFilter(field_name='author', label='Автор',
                               lookup_expr='exact', queryset=Author.objects.all())
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) информация о товарах

    class Meta:
        model = Post
        # поля, которые мы будем фильтровать (т.е. отбирать по каким-то критериям, имена берутся из моделей)
        # fields = ('time', 'tittle', 'author')
        fields = {
            # Цена должна быть меньше или равна тому, что указал пользователь
            'time': ['gt'],
            # Мы хотим чтобы нам выводило имя, хотя бы отдалённо похожее на то, что запросил пользователь
            'tittle': ['icontains'],
        }
