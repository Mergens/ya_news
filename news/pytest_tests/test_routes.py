# test_routes.py
from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects

import pytest


@pytest.mark.django_db
@pytest.mark.parametrize(
    'page, args',
    (
        ('news:detail', pytest.lazy_fixture('pk_news_for_args')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:home', None)
    )
)
def test_pages_availability_for_anonymous_user(args, client, page):
    """Тестирует доступ анонимного пользователя к страницам проекта"""
    url = reverse(page, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK

@pytest.mark.django_db
@pytest.mark.parametrize(
    'user_client, status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('not_author_client'), HTTPStatus.NOT_FOUND)
    )
)
@pytest.mark.parametrize(
    'page',
    ('news:edit', 'news:delete')
)
def test_availability_for_comment_edit_and_delete(
    comment, page, status, user_client
):
    """
    Тестирует возможность редактирования и удаления
    комментариев пользователями.
    """
    url = reverse(page, args=(comment.pk,))
    response = user_client.get(url)
    assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'page',
    ('news:edit', 'news:delete')
)
def test_redirect_for_anonymous_client(client, comment, page):
    """
    Тестирует перенаправление анонимного
    пользователя на страницу логина.
    """
    login_url = reverse('users:login')
    url = reverse(page, args=(comment.pk,))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)