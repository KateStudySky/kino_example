import pytest
import allure
import json
from data.test_data import (
    API_SEARCH_QUERY,
    INVALID_API_KEY,
    NON_EXISTENT_QUERY,
    YEAR_FOR_FILTER,
    GENRE_FOR_FILTER,
    RATING_MIN,
    RATING_MAX,
)
from api.api_client import APIClient


@allure.feature("API")
@allure.story("Поиск")
@pytest.mark.api
def test_search_movie_by_name(api_client):
    """
    Поиск фильма по названию.
    Проверяет, что запрос возвращает статус 200 и список фильмов не пуст.
    """
    with allure.step(f'Отправить запрос на поиск фильма "{API_SEARCH_QUERY}"'):
        response = api_client.search_movie(API_SEARCH_QUERY)

    with allure.step("Проверить статус-код 200"):
        assert (
            response.status_code == 200
        ), f"Ожидался 200, получен {response.status_code}"

    resp_body = response.json()

    with allure.step('Проверить, что ответ содержит поле "docs"'):
        assert "docs" in resp_body, 'Ответ не содержит поле "docs"'

    with allure.step("Проверить, что список фильмов не пуст"):
        assert len(resp_body["docs"]) > 0, "Список фильмов пуст"

    allure.attach(
        json.dumps(resp_body, indent=4, ensure_ascii=False),
        name="API Response",
        attachment_type=allure.attachment_type.JSON,
    )


# ====================================================================
#  ПОДСКАЗКИ ДЛЯ ОСТАЛЬНЫХ 4‑х API-ТЕСТОВ
#  Напиши их в этом же файле, используя готовый пример выше.
# ====================================================================

# 1. test_invalid_token()
#    📌 Что проверяем: отправка запроса с неверным API-ключом.
#    Шаги:
#      1. Импортируй INVALID_API_KEY из data.test_data.
#      2. Создай клиент с неверным ключом:
#         bad_client = APIClient(api_key=INVALID_API_KEY)
#      3. Отправь запрос на поиск фильма "Матрица":
#         response = bad_client.search_movie('Матрица')
#      4. Проверь статус-код 401.
#      5. Проверь, что в теле ответа есть слово "некорректен".
#    Пример проверок:
#         assert response.status_code == 401
#         assert 'некорректен' in response.text


# 2. test_search_non_existent()
#    📌 Что проверяем: поиск по несуществующему запросу.
#    Шаги:
#      1. Импортируй NON_EXISTENT_QUERY из data.test_data.
#      2. Отправь запрос: api_client.search_movie(NON_EXISTENT_QUERY)
#      3. Проверь статус-код 200.
#      4. Проверь, что поле docs – пустой список.
#      5. Проверь, что поле total равно 0.
#    Пример проверок:
#         assert response.status_code == 200
#         data = response.json()
#         assert data.get('docs') == []
#         assert data.get('total') == 0


# 3. test_movies_by_year_and_genre()
#    📌 Что проверяем: фильтрация по году и жанру.
#    Шаги:
#      1. Импортируй YEAR_FOR_FILTER и GENRE_FOR_FILTER из data.test_data.
#      2. Отправь запрос: api_client.get_movies_by_year_and_genre(YEAR_FOR_FILTER, GENRE_FOR_FILTER)
#      3. Проверь статус-код 200.
#      4. Проверь, что список фильмов не пуст.
#      5. Проверь у первых 5 фильмов:
#          - год равен YEAR_FOR_FILTER
#          - в списке жанров есть GENRE_FOR_FILTER
#    Пример проверок:
#         assert response.status_code == 200
#         data = response.json()
#         docs = data.get('docs', [])
#         assert len(docs) > 0
#         for film in docs[:5]:
#             assert film.get('year') == YEAR_FOR_FILTER
#             genres = [g.get('name') for g in film.get('genres', [])]
#             assert GENRE_FOR_FILTER in genres


# 4. test_movies_by_rating()
#    📌 Что проверяем: фильтрация по рейтингу IMDB.
#    Шаги:
#      1. Импортируй RATING_MIN и RATING_MAX из data.test_data.
#      2. Отправь запрос: api_client.get_movies_by_rating(RATING_MIN, RATING_MAX)
#      3. Проверь статус-код 200.
#      4. Проверь, что список фильмов не пуст.
#      5. Проверь у первых 5 фильмов, что rating.imdb (если есть) находится в диапазоне.
#    Пример проверок:
#         assert response.status_code == 200
#         data = response.json()
#         docs = data.get('docs', [])
#         assert len(docs) > 0
#         for film in docs[:5]:
#             rating = film.get('rating', {}).get('imdb')
#             if rating is not None:
#                 assert RATING_MIN <= rating <= RATING_MAX
