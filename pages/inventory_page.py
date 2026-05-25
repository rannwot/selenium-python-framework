from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    PRODUCT_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    PRODUCT_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")

    SORT_OPTIONS = {
        "name_asc": "Name (A to Z)",
        "name_desc": "Name (Z to A)",
        "price_asc": "Price (low to high)",
        "price_desc": "Price (high to low)",
    }

    def wait_until_loaded(self):
        self.wait.until(EC.visibility_of_element_located(self.INVENTORY_CONTAINER))

    def is_loaded(self):
        self.wait_until_loaded()
        return True

    def get_product_names(self):
        return [el.text for el in self.find_all(self.PRODUCT_NAMES)]

    def get_product_prices(self):
        prices = []
        for el in self.find_all(self.PRODUCT_PRICES):
            value = el.text.replace("$", "").strip()
            prices.append(float(value))
        return prices

    def sort_by(self, option_key):
        from selenium.webdriver.support.ui import Select

        dropdown = self.find(self.SORT_DROPDOWN)
        Select(dropdown).select_by_visible_text(self.SORT_OPTIONS[option_key])

    def get_cart_item_count(self):
        badges = self.driver.find_elements(*self.CART_BADGE)
        if badges and badges[0].is_displayed():
            return int(badges[0].text)
        return 0

    def wait_for_cart_count(self, expected):
        self.wait.until(lambda _: self.get_cart_item_count() == expected)

    def add_product_to_cart_by_index(self, index=0):
        expected = self.get_cart_item_count() + 1
        buttons = self.find_all(self.ADD_TO_CART_BUTTONS)
        data_test = buttons[index].get_attribute("data-test")
        self.click((By.CSS_SELECTOR, f"[data-test='{data_test}']"))
        self.wait_for_cart_count(expected)

    def add_product_to_cart_by_name(self, product_name):
        expected = self.get_cart_item_count() + 1
        add_button = (
            By.XPATH,
            f"//div[contains(@class,'inventory_item')]"
            f"[.//div[@data-test='inventory-item-name' and text()='{product_name}']]"
            f"//button[contains(@data-test,'add-to-cart')]",
        )
        self.click(add_button)
        self.wait_for_cart_count(expected)

    def go_to_cart(self):
        self.click(self.CART_LINK)
        self.wait.until(lambda driver: "cart" in driver.current_url)
