from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_LIST = (By.CSS_SELECTOR, "[data-test='inventory-item']")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "[data-test='checkout']")
    CART_ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")

    def is_loaded(self):
        return self.is_visible(self.CHECKOUT_BUTTON)

    def get_cart_item_names(self):
        return [el.text for el in self.find_all(self.CART_ITEM_NAMES)]

    def get_cart_item_count(self):
        return len(self.find_all(self.CART_LIST))

    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
        self.wait.until(lambda driver: "checkout-step-one" in driver.current_url)
