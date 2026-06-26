import pytest
import allure
from pages.main_page import MainPage
from data.test_data import SEARCH_QUERY, EXPECTED_MOVIE


@allure.feature("UI")
@allure.story("Поиск")
@pytest.mark.ui
def test_search_existing_movie(driver):
    """
    Поиск фильма по названию.
    Проверяет, что в результатах поиска есть ожидаемый фильм.
    """
    with allure.step(f'Открыть главную страницу и выполнить поиск "{SEARCH_QUERY}"'):
        main_page = MainPage(driver)
        search_results = main_page.search(SEARCH_QUERY)

    with allure.step(f'Проверить, что фильм "{EXPECTED_MOVIE}" присутствует'):
        assert search_results.is_movie_present(EXPECTED_MOVIE), \
            f'Фильм "{EXPECTED_MOVIE}" не найден'

    allure.attach(
        driver.get_screenshot_as_png(),
        name="search_result",
        attachment_type=allure.attachment_type.PNG,
    )


# ====================================================================
#  ПОДСКАЗКИ ДЛЯ ОСТАЛЬНЫХ 4‑х UI-ТЕСТОВ (без авторизации)
# ====================================================================

# 1. test_go_to_online_cinema()
#    Проверяет переход в онлайн-кинотеатр по ссылке в шапке.
#
#    Шаги:
#      1. На главной странице найти ссылку "Онлайн-кинотеатр" (локатор уже есть в main_page)
#      2. Кликнуть по ней
#      3. Проверить, что URL содержит "hd.kinopoisk.ru"
#
#    Используй: main_page.go_to_online_cinema()
#    Проверка: assert "hd.kinopoisk.ru" in driver.current_url

# 2. test_open_film_page_from_search()
#    Проверяет, что после поиска можно перейти на страницу первого найденного фильма.
#
#    Шаги:
#      1. Выполнить поиск через main_page.search(SEARCH_QUERY)
#      2. Открыть первый фильм через search_results.open_first_movie()
#      3. Проверить, что URL содержит "/film/"
#
#    Проверка: assert "/film/" in driver.current_url

# 3. test_filter_by_year_and_genre()
#    Проверяет фильтрацию каталога по году и жанру.
#
#    Шаги:
#      1. На главной странице найти выпадающие списки для года и жанра
#         (локаторы уже есть в main_page: YEAR_SELECT, GENRE_SELECT)
#      2. Выбрать год = 2023, жанр = "криминал"
#      3. Применить фильтр (нажать кнопку "Показать")
#      4. Проверить, что в результатах у первых 5 фильмов год = 2023 и жанр содержит "криминал"
#
#    Подсказка: используй Select из selenium.webdriver.support.ui
#    Пример: Select(driver.find_element(By.NAME, "year")).select_by_visible_text("2023")

# 
