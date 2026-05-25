import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config import PASSWORD, USERS


@pytest.fixture(scope="function")
def driver(request):
    """Create a fresh Chrome WebDriver for each test."""
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(0)
    yield browser
    browser.quit()


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )


@pytest.fixture
def login_page(driver):
    return LoginPage(driver)


@pytest.fixture
def inventory_page(driver):
    return InventoryPage(driver)


@pytest.fixture
def cart_page(driver):
    return CartPage(driver)


@pytest.fixture
def checkout_page(driver):
    return CheckoutPage(driver)


@pytest.fixture
def logged_in_inventory(login_page, inventory_page):
    """Log in with the standard user and return the inventory page."""
    login_page.open().login(USERS["standard"], PASSWORD)
    assert inventory_page.is_loaded(), "Inventory page did not load after login"
    return inventory_page
