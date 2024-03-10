"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
+ создать соответствующую модель (в models.py)
+ создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
+ заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
+ реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
+ по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from datetime import datetime, timedelta

from challenges.models import Post


HTTP_RESPONSE_404 = HttpResponse('', status=404)
HTTP_RESPONSE_403 = HttpResponse('', status=403)


def last_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    posts = Post.objects.filter(status='published').order_by('-published_at')[:3]
    if not posts:
        return HTTP_RESPONSE_404
    content = [post.to_json() for post in posts]
    return HttpResponse(str(content), status=200)


def posts_search_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    query = request.GET.get('query')
    if not query:
        return HTTP_RESPONSE_403
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(text__icontains=query))
    if not posts:
        return HTTP_RESPONSE_404
    content = [post.to_json() for post in posts]
    return HttpResponse(str(content), status=200)


def untagged_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    posts = Post.objects.filter(category__isnull=True).order_by('author__first_name', 'created_at')
    if not posts:
        return HTTP_RESPONSE_404
    content = [post.to_json() for post in posts]
    return HttpResponse(str(content), status=200)


def categories_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    categories_raw = request.GET.get('categories')
    if not categories_raw:
        return HTTP_RESPONSE_403
    categories = categories_raw.strip().split(',')
    posts = Post.objects.filter(category__in=categories)
    if not posts:
        return HTTP_RESPONSE_404
    content = [post.to_json() for post in posts]
    return HttpResponse(str(content), status=200)


def last_days_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    last_days_raw = request.GET.get('last_days')

    if not last_days_raw:
        return HTTP_RESPONSE_403

    try:
        last_days = int(last_days_raw)
    except ValueError:
        return HTTP_RESPONSE_403

    last_days_date = datetime.now() - timedelta(days=last_days)

    posts = Post.objects.filter(published_at__gte=last_days_date)
    if not posts:
        return HTTP_RESPONSE_404
    content = [post.to_json() for post in posts]
    return HttpResponse(str(content), status=200)
