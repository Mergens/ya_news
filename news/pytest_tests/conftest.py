# conftest.py
import pytest
from datetime import datetime

# Импортируем класс клиента.
from django.test.client import Client
from django.db import models

# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import News, Comment


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):  # Вызываем фикстуру автора.
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)  # Логиним обычного пользователя в клиенте.
    return client


@pytest.fixture
def news():
    """Новость."""
    news = News.objects.create(
        title='Заголовок',
        text='Текст новости',
    )
    return news


@pytest.fixture
def pk_news_for_args(news):
    """Возвращаем id новости."""
    return (news.id,)


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )
    return comment


@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def slug_for_args(news):
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return (news.slug,)
