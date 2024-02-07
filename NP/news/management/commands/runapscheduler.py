# runapscheduler.py
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ...models import Post, Category, User

import datetime

logger = logging.getLogger(__name__)


def my_job():
    # Создаем класс для контекстного объекта передачи данных в шаблон
    class Subscrib:
        user = ''

    # Находим дату недельной давности:
    minus_week = datetime.datetime.now() - datetime.timedelta(days=7)
    # Формируем список всех экземпляров Category
    category_set = Category.objects.all()
    # Формируем словарь вида с пустыми списками под теги {category_name: [], ...}
    category_post_dict = {}
    # и словарь списков пользователей по ключю category:
    subscribers_by_category = {}
    for i in category_set:
        category = i.category
        # print('category is', category)
        category_post_dict[i.category] = []
        post_list = Post.objects.filter(category=i.id, time__gt=minus_week)

        # Формируем списки пользователей по категориям для ограничения обращений к БД
        subscribers_dict = Category.objects.filter(category=i.category).values(
            'subscribers__email')
        # print('subscribers_dict is:', subscribers_dict)
        subscribers_list = []
        [subscribers_list.append(subscriber['subscribers__email'])
            for subscriber in subscribers_dict]
        subscribers_by_category[i.category] = subscribers_list
        print('subscribers_by_category is: ', subscribers_by_category)

        # Пополняем словарь по категориям списком тегов {category_name: [href_tag_Post, ...], ...}:
        for j in post_list:
            tag = f'<a href="http://127.0.0.1:8000/news/{j.id}">Статья {j.tittle}</a><br>'
            category_post_dict[i.category].append(tag)
        # print('category_post_dict is:', category_post_dict)

    # Формируем множество кортежей данных подписчиков {(username, email), ...}:
    subscribers_dict = Category.objects.all().values(
        'subscribers__username', 'subscribers__email')
    # print('subscribers_dict is ', subscribers_dict)
    subscribers_list = []
    [subscribers_list.append(
        (i['subscribers__username'], i['subscribers__email'])) for i in subscribers_dict]
    # print('subscribers_list is ', subscribers_list)
    subscribers_set = set(subscribers_list) - {(None, None)}
    print('subscribers_set is ', subscribers_set)

    # Формируем список тегов по постам за неделю для каждого подписчика
    for subscriber in subscribers_set:
        user = subscriber[0]
        email = subscriber[1]
        tag_list = []
        print('------------------------------------------')
        print('user is: ', user)
        for cat in subscribers_by_category:
            print('-------')
            print(cat)
            print('subscribers_by_category[cat] is : ',
                  subscribers_by_category[cat])
            if email in subscribers_by_category[cat]:
                print('user in Category', cat)
                # tag_list.append(category_post_dict[cat])
                tag_list += category_post_dict[cat]
        tag_list = list(set(tag_list))
        print('tag_list is: ', tag_list)

        # Формируем объект для передачи контекста
        context_obj = Subscrib()
        context_obj.user = user
        context_obj.tag_list = tag_list
        # привязываем наш html и контекстный объект
        html_content = render_to_string(
            'weekly_email.html',
            {
                'context_obj': context_obj,
            }
        )
        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f"Подписка NewsPaper: Еженедельная сводка",
            # это то же, что и message
            body=f"Здравствуй, {user}. Сводка новостей за неделю по Вашей подписке! {tag_list}",
            from_email='sabanchini@yandex.ru',
            to=[email],  # это то же, что и recipients_list
        )
        msg.attach_alternative(
            html_content, "text/html")  # добавляем html
        msg.send()


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=2_592_000):
    # def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            # 1 AM on every Monday.
            trigger=CronTrigger(day_of_week="mon", hour="01", minute="00"),
            # trigger=CronTrigger(second="*/604800"),  # Every 10 seconds
            # id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
