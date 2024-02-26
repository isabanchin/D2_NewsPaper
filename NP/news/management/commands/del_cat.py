from django.core.management.base import BaseCommand, CommandError
from ...models import Category, Post


class Command(BaseCommand):
    help = 'Run command, input Category from list, confirm if you sure'

    def handle(self, *args, **options):
        category_list = Category.objects.all()
        for category in category_list:
            self.stdout.write(category.category)
        cat_selection = input('Input one category to delete from upper list: ')
        try:
            post_list = Post.objects.filter(
                category=Category.objects.get(category=cat_selection))
        except category.DoesNotExist:
            raise CommandError('category "%s" does not exist' % cat_selection)
        else:
            self.stdout.write(
                'Do you really want to delete all posts? yes/no')
            answer = input()  # считываем подтверждение
            if answer == 'yes':
                for post in post_list:
                    self.stdout.write(f'To delete post tittle: {post.tittle}')
                    post.delete()
                self.stdout.write(self.style.SUCCESS(
                    'Succesfully wiped posts!'))
