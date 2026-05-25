from selenium.common.exceptions import (
    ElementNotInteractableException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.config import DEFAULT_TIMEOUT


class BasePage:
    """Shared WebDriver helpers for all page objects."""

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

    def click(self, locator, retries=3):
        last_error = None
        for _ in range(retries):
            try:
                element = self.find_clickable(locator)
                self.driver.execute_script("arguments[0].click();", element)
                return
            except (ElementNotInteractableException, StaleElementReferenceException) as exc:
                last_error = exc
        raise last_error

    def navigation_click(self, locator, url_fragment, retries=3, retry_wait=15):
        """Click a navigation element and confirm URL changes, retrying if needed.

        Uses a short per-attempt window so a slow page load that outlasts
        retry_wait is detected (via the URL check at the top of each loop)
        before a stale-locator re-click is attempted on the wrong page.
        """
        short_wait = WebDriverWait(self.driver, retry_wait)
        for attempt in range(retries):
            if url_fragment in self.driver.current_url:
                return  # already navigated (slow load finished between retries)
            element = self.find_clickable(locator)
            self.driver.execute_script("arguments[0].click();", element)
            try:
                short_wait.until(EC.url_contains(url_fragment))
                return
            except TimeoutException:
                if url_fragment in self.driver.current_url:
                    return  # navigation completed during the wait window
                if attempt == retries - 1:
                    self.wait.until(EC.url_contains(url_fragment))

    def type_text(self, locator, text, retries=3):
        last_error = None
        for _ in range(retries):
            try:
                element = self.find_clickable(locator)
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", element
                )
                element.click()
                element.clear()
                element.send_keys(text)
                return
            except (ElementNotInteractableException, StaleElementReferenceException) as exc:
                last_error = exc
        raise last_error

    def get_text(self, locator):
        return self.find(locator).text

    def is_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except Exception:
            return False
