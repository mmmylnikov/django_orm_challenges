"""
В этом задании вам предстоит работать с моделью ноутбука. У него есть бренд (один из нескольких вариантов),
год выпуска, количество оперативной памяти, объём жесткого диска, цена, количество этих ноутбуков на складе
и дата добавления.

Ваша задача:
+ создать соответствующую модель (в models.py)
+ создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
+ заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
  (я бы советовал использовать для этого shell)
+ реализовать у модели метод to_json, который будет преобразовывать объект ноутбука в json-сериализуемый словарь
+ по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from django.http import HttpRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from challenges.models import Laptop
import json


HTTP_RESPONSE_404 = HttpResponse('', status=404)
HTTP_RESPONSE_403 = HttpResponse('', status=403)


def laptop_details_view(request: HttpRequest, laptop_id: int) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание ноутбука по его id.
    Если такого id нет, вернуть 404.
    """
    try:
        laptop = Laptop.objects.get(id=laptop_id)
    except ObjectDoesNotExist:
        return HTTP_RESPONSE_404
    return HttpResponse(str(laptop.to_json()), status=200)


def laptop_in_stock_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание всех ноутбуков, которых на складе больше нуля.
    Отсортируйте ноутбуки по дате добавления, сначала самый новый.
    """
    laptops = Laptop.objects.filter(quantity__gt=0).order_by('-created_at')
    content = [laptop.to_json() for laptop in laptops]
    return HttpResponse(str(content), status=200)


def laptop_filter_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть список ноутбуков с указанным брендом и указанной минимальной ценой.
    Бренд и цену возьмите из get-параметров с названиями brand и min_price.
    Если бренд не входит в список доступных у вас на сайте или если цена отрицательная, верните 403.
    Отсортируйте ноутбуки по цене, сначала самый дешевый.
    """
    brand_raw = request.GET.get('brand')
    min_price_raw = request.GET.get('min_price')

    laptops = Laptop.objects.all()

    if brand_raw:
        if brand_raw not in [brand for brand, _ in Laptop.brand.field.choices]:
            return HTTP_RESPONSE_403
        laptops = laptops.filter(brand=brand_raw)

    if min_price_raw:
        try:
            min_price = float(min_price_raw)
        except ValueError:
            return HTTP_RESPONSE_403
        if min_price < 0:
            return HTTP_RESPONSE_403
        laptops = laptops.filter(amount__gte=min_price)

    laptops = laptops.order_by('amount')
    content = [laptop.to_json() for laptop in laptops]
    return HttpResponse(str(content), status=200)


def last_laptop_details_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание последнего созданного ноутбука.
    Если ноутбуков нет вообще, вернуть 404.
    """
    last_laptop = Laptop.objects.order_by('created_at').last()
    if not last_laptop:
        return HTTP_RESPONSE_404
    return HttpResponse(str(last_laptop.to_json()), status=200)
