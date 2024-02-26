from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment

# напишем уже знакомую нам функцию обнуления товара на складе


# все аргументы уже должны быть вам знакомы, самые нужные из них это request — объект хранящий информацию о запросе и queryset — грубо говоря набор объектов, которых мы выделили галочками.
def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)
    # описание для более понятного представления в админ панеле задаётся, как будто это объект
    nullfy_rating.short_description = 'Рейтинг поста = 0'


def one_rating(modeladmin, request, queryset):
    queryset.update(rating=1)
    # описание для более понятного представления в админ панеле задаётся, как будто это объект
    one_rating.short_description = 'Рейтинг поста = 1'

# создаём новый класс для представления постов в админке


class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице постов
    # генерируем список имён всех полей для более красивого отображения
    list_display = ('id', 'author', 'tittle', 'time', 'type', 'rating')
    # list_display = [field.name for field in Post._meta.get_fields()[2:9]]
    # добавляем примитивные фильтры в нашу админку
    list_filter = ('type', 'author')
    # тут всё очень похоже на фильтры из запросов в базу
    search_fields = ('tittle', 'text')
    actions = [nullfy_rating, one_rating]  # добавляем действия в список


class CommentAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице постов
    # генерируем список имён всех полей для более красивого отображения
    list_display = [field.name for field in Comment._meta.get_fields()]
    # добавляем примитивные фильтры в нашу админку
    list_filter = ('user', )
    # тут всё очень похоже на фильтры из запросов в базу
    search_fields = ('tittle', 'text')


class AuthorAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице постов
    # генерируем список имён всех полей для более красивого отображения
    list_display = [field.name for field in Author._meta.get_fields()[1:]]
    # list_display = ('id', 'post', 'user', 'text', 'time', 'rating')
    # # добавляем примитивные фильтры в нашу админку
    # list_filter = ('user', )
    # # тут всё очень похоже на фильтры из запросов в базу
    # search_fields = ('tittle', 'text')


class PostCategoryAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице постов
    # генерируем список имён всех полей для более красивого отображения
    list_display = [field.name for field in PostCategory._meta.get_fields()]
    # list_display = ('id', 'post', 'user', 'text', 'time', 'rating')
    # добавляем примитивные фильтры в нашу админку
    list_filter = ('category', )
    # тут всё очень похоже на фильтры из запросов в базу
    # search_fields = ('post', )


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
