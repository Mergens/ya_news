import pytest
from http import HTTPStatus
from django.urls import reverse
from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


class TestComments():
    COMMENT_TEXT = 'Текст комментария'
    form_data = {'text': COMMENT_TEXT}

    @pytest.mark.django_db
    def test_anonymous_user_cant_create_comment(self, client, news):
        url = reverse('news:detail', args=(news.id,))
        client.post(url, data=self.form_data)
        comment_count = Comment.objects.count()
        assert comment_count == 0

    @pytest.mark.django_db
    def test_user_can_create_comment(self, author, author_client, news):
        url = reverse('news:detail', args=(news.id,))
        response = author_client.post(url, data=self.form_data)
        assertRedirects(response, f'{url}#comments')
        comments_count = Comment.objects.count()
        assert comments_count == 1
        comment = Comment.objects.get()
        assert comment.text == self.COMMENT_TEXT
        assert comment.news == news
        assert comment.author == author

    @pytest.mark.django_db
    def test_author_can_delete_comment(self, author_client, news, comment):
        news_url = reverse('news:detail', args=(news.id,))
        url_to_comments = news_url + '#comments'

        url = reverse('news:delete', args=(comment.id,))
        response = author_client.delete(url)
        assertRedirects(response, url_to_comments)
        comments_count = Comment.objects.count()
        assert comments_count == 0

    @pytest.mark.django_db
    def test_user_cant_edit_comment_of_another_user(
            self, not_author_client, comment):

        comment_text_before = comment.text
        self.form_data['text'] = self.COMMENT_TEXT
        edit_url = reverse('news:edit', args=(comment.id,))
        response = not_author_client.post(edit_url, data=self.form_data)
        assert response.status_code == HTTPStatus.NOT_FOUND
        comment.refresh_from_db()
        assert comment.text == comment_text_before


@pytest.mark.django_db
def test_user_cant_use_bad_words(author_client, news):
    url = reverse('news:detail', args=(news.id,))
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, ещё текст'}
    response = author_client.post(url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0
