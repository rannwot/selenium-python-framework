from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    FIRST_NAME = (By.CSS_SELECTOR, "[data-test='firstName']")
    LAST_NAME = (By.CSS_SELECTOR, "[data-test='lastName']")
    POSTAL_CODE = (By.CSS_SELECTOR, "[data-test='postalCode']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "[data-test='continue']")
    FINISH_BUTTON = (By.CSS_SELECTOR, "[data-test='finish']")
    CANCEL_BUTTON = (By.CSS_SELECTOR, "[data-test='cancel']")
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")
    SUBTOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def wait_for_info_step(self):
        self.wait.until(EC.url_contains("checkout-step-one"))
        self.wait.until(EC.visibility_of_element_located(self.FIRST_NAME))
        self.wait.until(
            EC.text_to_be_present_in_element(
                self.TITLE, "Checkout: Your Information"
            )
        )

    def wait_for_overview_step(self):
        self.wait.until(EC.url_contains("checkout-step-two"))
        self.wait.until(
            EC.text_to_be_present_in_element(self.TITLE, "Checkout: Overview")
        )

    def fill_shipping_info(self, first_name, last_name, postal_code):
        self.wait_for_info_step()
        self.driver.execute_script(
            """
            function setVal(sel, val) {
                if (!val) return;
                var el = document.querySelector(sel);
                var setter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value'
                ).set;
                setter.call(el, val);
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
            }
            setVal("[data-test='firstName']", arguments[0]);
            setVal("[data-test='lastName']", arguments[1]);
            setVal("[data-test='postalCode']", arguments[2]);
            """,
            first_name,
            last_name,
            postal_code,
        )
        self.find_clickable(self.CONTINUE_BUTTON).click()
        if first_name and last_name and postal_code:
            self.wait.until(EC.url_contains("checkout-step-two"))
        else:
            self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))

    def get_overview_title(self):
        self.wait_for_overview_step()
        return self.get_text(self.TITLE)

    def get_subtotal(self):
        self.wait_for_overview_step()
        text = self.get_text(self.SUBTOTAL)
        return float(text.split("$")[1])

    def finish_order(self):
        self.wait_for_overview_step()
        self.find_clickable(self.FINISH_BUTTON).click()
        self.wait.until(EC.url_contains("checkout-complete"))
        self.wait.until(
            EC.text_to_be_present_in_element(
                self.COMPLETE_HEADER, "Thank you for your order!"
            )
        )

    def get_completion_message(self):
        return self.get_text(self.COMPLETE_HEADER)

    def is_error_displayed(self):
        try:
            self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE))
            return True
        except TimeoutException:
            return False

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)
