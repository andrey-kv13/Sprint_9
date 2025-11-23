from locators.main_page_locators import MainPageLocators as mpl
from pages.base_page import BasePage

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        
    def click_create_acc_button(self):
        self.click(mpl.CREATE_ACC_BUTTON)
    
    def click_login_button(self):
        self.click(mpl.LOGIN_BUTTON)
        
    def click_create_recipe_button(self):
        self.click(mpl.CREATE_RECIPET_BUTTON)
        
    def get_recipes_label_text(self):
        return self.get_element_text(mpl.RECIPES_LABEL)
    
    def is_logout_button_displayed(self):
        """Проверяет, отображается ли кнопка 'Выход'"""
        element = self.find_element(mpl.LOGOUT_BUTTON)
        return element is not None