from django.db import models
from django.core import serializers
from django.contrib.auth.models import User
import json


class InstanceToJsonMixin:
    def to_json(self) -> dict:
        return json.loads(serializers.serialize(
            'json', [self], ensure_ascii=False)[1:-1])


class Book(InstanceToJsonMixin, models.Model):
    title = models.CharField(max_length=256)
    author_full_name = models.CharField(max_length=256)
    isbn = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Laptop(InstanceToJsonMixin, models.Model):
    brand = models.CharField(
        max_length=64,
        choices=[
            ('apple', 'Apple'),
            ('hp', 'Hewlett-Packard'),
            ('acer', 'Acer'),
            ('lenovo', 'Lenovo'),
        ],
        verbose_name='Бренд'
    )
    release_year = models.DateField(verbose_name='Бренд')
    ram = models.PositiveSmallIntegerField(verbose_name='Объем ОЗУ')
    hdd = models.PositiveSmallIntegerField(verbose_name='Объем HDD')
    amount = models.FloatField(verbose_name='Цена')
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество на складе')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='Обновлено')

    def __str__(self):
        output = self.get_brand_display() + ' '
        output += str(self.release_year.year) + '/'
        output += 'RAM ' + str(self.ram) + 'GB/'
        output += 'HDD ' + str(self.hdd) + 'GB'
        return output

    class Meta:
        ordering = ['-release_year']
        get_latest_by = 'release_year'
        verbose_name = 'Ноутбук'
        verbose_name_plural = 'Ноутбуки'


class Post(InstanceToJsonMixin, models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User, on_delete=models.PROTECT, verbose_name='Автор')
    status = models.CharField(
        max_length=9,
        choices=[
            ('published', 'опубликован'),
            ('draft', 'не опубликован'),
            ('banned', 'забанен'),
        ],
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлен')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    published_at = models.DateTimeField(null=True, verbose_name='Опубликован')
    category = models.CharField(
        max_length=4,
        null=True,
        choices=[
            ('home', 'дом'),
            ('work', 'работа'),
            ('dev', 'разработка'),
        ],
        verbose_name='Категория'
    )

    def __str__(self):
        output = self.title + ' '
        output += '(' + self.get_category_display() + '), '
        output += self.author.first_name
        return output

    class Meta:
        ordering = ['-published_at']
        get_latest_by = 'published_at'
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
