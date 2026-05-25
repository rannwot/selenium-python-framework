from selenium.webdriver.common.by import By

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

    def is_loaded(self):
        return self.is_visible(self.INVENTORY_CONTAINER)

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

    def add_product_to_cart_by_index(self, index=0):
        buttons = self.find_all(self.ADD_TO_CART_BUTTONS)
        buttons[index].click()

    def add_product_to_cart_by_name(self, product_name):
        add_button = (
            By.XPATH,
            f"//div[contains(@class,'inventory_item')]"
            f"[.//div[@data-test='inventory-item-name' and text()='{product_name}']]"
            f"//button[contains(@data-test,'add-to-cart')]",
        )
        self.click(add_button)

    def get_cart_item_count(self):
        if self.is_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0

    def go_to_cart(self):
        self.click(self.CART_LINK)
