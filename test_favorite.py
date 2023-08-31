import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

FAVORITE_BUTTON_DIV_XPATH = f"//div[starts-with(@class,\"style-header-add-favorite\")]"


# Wait for elements
def wait_of_element_located(xpath, driver_init):
    element = WebDriverWait(driver_init, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)
        )
    )
    return element


def wait_of_element_disappear(xpath, driver_init):
    element = WebDriverWait(driver_init, 10).until_not(
        EC.presence_of_element_located(
            (By.XPATH, xpath)
        )
    )
    return True


class TestAddToFavoriteButton:
    # init driver once
    @pytest.fixture(scope='class')
    def driver_init(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(options=options)
        driver.get(
            "https://www.avito.ru/nikel/knigi_i_zhurnaly/domain-driven_design_distilled_vaughn_vernon_2639542363")
        yield driver
        driver.close()

    @pytest.fixture
    def add_item_to_favorite(self, driver_init):
        item_add_button = wait_of_element_located(
            xpath=f"{FAVORITE_BUTTON_DIV_XPATH}/button",
            driver_init=driver_init)

        assert wait_of_element_located(xpath=f'{FAVORITE_BUTTON_DIV_XPATH}/button/*[name('
                                             ')=\'svg\' and @data-icon=\'favorites\']',
                                       driver_init=driver_init) is not None, "assert favorite icon is unfilled"

        button_span = wait_of_element_located(
            xpath=f'{FAVORITE_BUTTON_DIV_XPATH}/button/*[name()=\'span\']',
            driver_init=driver_init)

        assert button_span.text == "Добавить в избранное", "assert button is not clicked"

        item_add_button.click()

    def test_add_item_to_favorite_success(self, driver_init, add_item_to_favorite):
        # Step 0: check popup
        popup = wait_of_element_located(xpath='//*[starts-with(text(),\"Добавлено\")]', driver_init=driver_init)
        assert popup.text == "Добавлено в избранное"
        assert wait_of_element_located(
            xpath='//*[starts-with(text(),\"Добавлено\")]/a[@href=\"/favorites/knigi_i_zhurnaly\"]',
            driver_init=driver_init) is not None, "assert link"

        # Popup supposed to be disappeared. But makes test longer
        assert wait_of_element_disappear(xpath='//*[starts-with(text(),\"Добавлено\")]', driver_init=driver_init)

        # Step 1: check icon
        assert wait_of_element_located(xpath=f'{FAVORITE_BUTTON_DIV_XPATH}/button/*[name('
                                             ')=\'svg\' and @data-icon=\'favorites-filled\']',
                                       driver_init=driver_init), "assert favorite icon is filled"

        # Step 2: check button span
        button_span = wait_of_element_located(
            xpath=f'{FAVORITE_BUTTON_DIV_XPATH}/button/*[name()=\'span\']',
            driver_init=driver_init)

        assert button_span.text == "В избранном", "assert button text is clicked"

        # Step 3: check button attrs
        item_add_button = wait_of_element_located(
            xpath=f"{FAVORITE_BUTTON_DIV_XPATH}/button",
            driver_init=driver_init)

        assert item_add_button.get_attribute("title") == "В избранном", "assert button title is clicked"
        assert item_add_button.get_attribute("data-is-favorite") == "true", "assert button state is clicked"
