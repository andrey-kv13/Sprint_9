from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.config import Config
from selenium.common.exceptions import TimeoutException

class BasePage:
    """Базовый класс с общими методами для работы со страницами"""

    def __init__(self, driver):
        self.driver = driver
        self.timeout = Config.TIMEOUT
        self.wait = WebDriverWait(driver, Config.TIMEOUT)

    def find_element(self, locator):
        """Поиск элемента с ожиданием его видимости"""       
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element
        except TimeoutException:
            return None

    def find_elements(self, locator):
        """Поиск всех элементов по локатору"""        
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            return []

    def find_element_by_presence(self, locator):
        """Поиск элемента по присутствию в DOM (не требует видимости)"""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            return None

    def scroll_to_element(self, locator):
        """Скролл к указанному элементу"""     
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)

    def click(self, locator):
        """Клик по элементу со скроллом и ожиданием кликабельности"""   
        try:
            self.scroll_to_element(locator)
            element = self.wait.until(EC.element_to_be_clickable(locator))
            # Пробуем обычный клик, если не получается - используем JavaScript
            try:
                element.click()
            except Exception:
                # Если элемент перекрыт, используем JavaScript клик
                self.driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            pass

    def send_keys(self, locator, text):
        """Ввод текста в поле"""
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            pass

    def get_element_text(self, locator):
        try:
            return self.find_element(locator).text
        except TimeoutException:
            return None

    def get_attribute(self, locator, attribute):
        try:
            return self.find_element(locator).get_attribute(attribute)
        except TimeoutException:
            return None

    def wait_page_url(self, url_part):
        """Ожидает, пока не откроется страница с указанной частью URL"""
        try:
            self.wait.until(EC.url_contains(url_part))
        except TimeoutException:
            return False
        return True

    def get_current_url(self):
        """Получает текущий URL страницы"""
        return self.driver.current_url

    def select_first_dropdown_item(self, dropdown_item_locator, dropdown_container_locator=None):
        """
        Выбирает первый элемент из выпадающего списка
        
        :param dropdown_item_locator: локатор первого элемента выпадающего списка
        :param dropdown_container_locator: опциональный локатор контейнера выпадающего списка
                                           для ожидания его появления перед кликом
        """
        # Если передан локатор контейнера, ждем его появления
        if dropdown_container_locator:
            self.find_element(dropdown_container_locator)
        # Кликаем по первому элементу из выпадающего списка
        self.click(dropdown_item_locator)