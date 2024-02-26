from django.db import models
# from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        user = self.user
        # Суммарный рейтинг постов автора:
        post_rating_list = Post.objects.filter(author=self).values('rating')
        post_rating = sum([post_rating_list[i]['rating']
                          for i in range(len(post_rating_list))])
        print('post_rating = ', post_rating)

        # Суммарный рейтинг комментариев автора:
        author_comments_rating_list = Comment .objects.filter(
            user=user).values('rating')
        author_comments_rating = sum([author_comments_rating_list[i]['rating']
                                     for i in range(len(author_comments_rating_list))])
        print('author_comments_rating = ', author_comments_rating)

        # Суммарный рейтинг комментариев под постами автора:
        post_list = Post.objects.filter(author=self)
        print(post_list)
        users_comments_rating = 0
        for i in range(len(post_list)):
            users_comments_rating = users_comments_rating + sum([Comment.objects.filter(post=post_list[i]).values(
                'rating')[j]['rating'] for j in range(len(Comment.objects.filter(post=post_list[i]).values('rating')))])
        print('users_comments_rating = ', users_comments_rating)

        # Совокупный рейтинг автора:
        self.rating = post_rating * 3 + author_comments_rating + users_comments_rating
        self.save()
        return self.rating

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return self.category


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = 'ARTICLE'
    news = 'NEWS'
    TYPE_CHOICES = (
        (article, 'Article'),
        (news, 'News')
    )
    type = models.CharField(
        max_length=7, choices=TYPE_CHOICES, default='article')
    time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    tittle = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
        return self.rating

    def dislike(self):
        self.rating -= 1
        self.save()
        return self.rating

    def preview(self):
        return self.text[:128] + '...'

    def __str__(self):
        return f'Post #{self.pk} - Tittle: {self.tittle}'

    # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        # сначала вызываем метод родителя, чтобы объект сохранился
        super().save(*args, **kwargs)
        # затем удаляем его из кэша, чтобы сбросить его
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # user = models.OneToOneField(
    # settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
        return self.rating

    def dislike(self):
        self.rating -= 1
        self.save()
        return self.rating
