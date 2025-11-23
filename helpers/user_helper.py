"""
Модуль с вспомогательными методами для работы с пользователями
(регистрация, авторизация и т.д.)
"""
from pages.main_page import MainPage
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from config.config import Config

class UserHelper:
    """Класс с методами для работы с пользователями"""
    
    def __init__(self, driver):
        self.driver = driver
        self.main_page = MainPage(driver)
        self.registration_page = RegistrationPage(driver)
        self.login_page = LoginPage(driver)
    
    def register_user(self):
        """
        Выполняет полную регистрацию пользователя
        """
        test_data = Config.test_data()
        user_name = test_data["username"]
        password = test_data["password"]
        self.main_page.click_create_acc_button()
        self.registration_page.populate_registration_data(user_name, password, test_data)
        return user_name, password
    
    def login_user(self, user_name, password):
        """
        Выполняет авторизацию пользователя
        """
        
        self.main_page.click_login_button()
        self.login_page.populate_login_data(user_name, password)
        self.login_page.click_login_button()
        return self.login_page
    
    def register_and_login_user(self):
        """
        Выполняет регистрацию и последующую авторизацию пользователя
        """
        user_name, password = self.register_user()
        # После регистрации обычно происходит переход на страницу входа
        self.login_user(user_name, password)
        # После успешной авторизации пользователь попадает на главную страницу
        return self.main_page

