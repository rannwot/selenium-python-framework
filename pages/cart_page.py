from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_LIST = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout']")
    CART_ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")

    def wait_until_loaded(self):
        self.wait.until(lambda driver: "cart" in driver.current_url)
        self.wait.until(EC.visibility_of_element_located(self.CHECKOUT_BUTTON))

    def is_loaded(self):
        self.wait_until_loaded()
        return True

    def get_cart_item_names(self):
        return [el.text for el in self.find_all(self.CART_ITEM_NAMES)]

    def get_cart_item_count(self):
        return len(self.find_all(self.CART_LIST))

    def proceed_to_checkout(self):
        element = self.find_clickable(self.CHECKOUT_BUTTON)
        self.driver.execute_script("arguments[0].click();", element)
        self.wait.until(EC.url_contains("checkout-step-one"))
