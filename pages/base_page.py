from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import DEFAULT_TIMEOUT


class BasePage:
    def __init__(self, driver, timeout=DEFAULT_TIMEOUT):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def _retry(self, action, retries=3):
        last_error = None
        for _ in range(retries):
            try:
                return action()
            except (ElementNotInteractableException, StaleElementReferenceException) as exc:
                last_error = exc
        raise last_error

    def click(self, locator, retries=3):
        def attempt():
            element = self.find_clickable(locator)
            self.driver.execute_script("arguments[0].click();", element)

        self._retry(attempt, retries)

    def navigation_click(self, locator, url_fragment):
        element = self.find_clickable(locator)
        self.driver.execute_script("arguments[0].click();", element)
        self.wait.until(EC.url_contains(url_fragment))

    def type_text(self, locator, text, retries=3):
        def attempt():
            element = self.find_clickable(locator)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});", element
            )
            self.driver.execute_script(
                """
                var el = arguments[0], val = arguments[1];
                var setter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value'
                ).set;
                setter.call(el, val);
                el.dispatchEvent(new Event('input', { bubbles: true }));
                el.dispatchEvent(new Event('change', { bubbles: true }));
                """,
                element,
                text,
            )

        self._retry(attempt, retries)

    def get_text(self, locator):
        return self.find(locator).text

    def is_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
