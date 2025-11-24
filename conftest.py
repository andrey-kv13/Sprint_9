from selenium import webdriver
import pytest
import os
from config.config import Config
from pages.main_page import MainPage
from pages.registration_page import RegistrationPage
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.recipe_page import RecipePage
from helpers.user_helper import UserHelper
from selenium.webdriver.chrome.options import Options as ChromeOptions

@pytest.fixture(scope="function")
def driver():
    """Фикстура для инициализации WebDriver"""
    use_remote = os.getenv("USE_REMOTE_DRIVER", "false").lower() == "true"

    if use_remote:
        # Используем Remote WebDriver для работы с Selenoid в Docker
        selenoid_uri = os.getenv("SELENOID_URI", "http://selenoid:4444/wd/hub")
        options = ChromeOptions()
        options.add_argument("--incognito")
        
        driver = webdriver.Remote(
            command_executor=selenoid_uri,
            options=options
        )
    else:
        # Используем локальный Chrome WebDriver
        options = ChromeOptions()
        options.add_argument("--incognito")
        driver = webdriver.Chrome(options=options)

    driver.maximize_window()
    driver.get(Config.BASE_URL)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def main_page(driver):
    return MainPage(driver)

@pytest.fixture(scope="function")
def registration_page(driver):
    return RegistrationPage(driver)

@pytest.fixture(scope="function")
def base_page(driver):
    return BasePage(driver)

@pytest.fixture(scope="function")
def login_page(driver):
    return LoginPage(driver)

@pytest.fixture(scope="function")
def recipe_page(driver):
    return RecipePage(driver)

@pytest.fixture(scope="function")
def user_helper(driver):
    """Фикстура для работы с пользователями (регистрация, авторизация)"""
    return UserHelper(driver)