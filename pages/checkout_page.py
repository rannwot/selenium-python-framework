from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "[data-test='continue']")
    FINISH_BUTTON = (By.CSS_SELECTOR, "[data-test='finish']")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "[data-test='cancel']")
    INFO_STEP_TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    OVERVIEW_TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")
    SUBTOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def wait_for_info_step(self):
        self.wait.until(
            lambda _: self.get_text(self.INFO_STEP_TITLE) == "Checkout: Your Information"
        )

    def fill_shipping_info(self, first_name, last_name, postal_code):
        self.wait_for_info_step()
        if first_name:
            self.type_text(self.FIRST_NAME, first_name)
        if last_name:
            self.type_text(self.LAST_NAME, last_name)
        if postal_code:
            self.type_text(self.POSTAL_CODE, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def get_overview_title(self):
        return self.get_text(self.OVERVIEW_TITLE)

    def get_subtotal(self):
        text = self.get_text(self.SUBTOTAL)
        return float(text.split("$")[1])

    def finish_order(self):
        self.click(self.FINISH_BUTTON)

    def get_completion_message(self):
        return self.get_text(self.COMPLETE_HEADER)

    def is_error_displayed(self):
        return self.is_visible(self.ERROR_MESSAGE)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)
