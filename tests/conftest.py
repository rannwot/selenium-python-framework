import os
import shutil

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config import PASSWORD, USERS


@pytest.fixture(scope="function")
def driver(request):
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    chrome_bin = os.getenv("CHROME_BIN")
    if chrome_bin:
        options.binary_location = chrome_bin

    chromedriver_path = os.getenv("CHROMEDRIVER_PATH") or shutil.which("chromedriver")
    if chromedriver_path:
        browser = webdriver.Chrome(
            service=Service(chromedriver_path), options=options
        )
    else:
        browser = webdriver.Chrome(options=options)

    browser.implicitly_wait(0)
    yield browser
    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            try:
                os.makedirs("reports", exist_ok=True)
                with open("reports/ci-debug.txt", "a") as f:
                    f.write(f"FAILED: {item.nodeid}\n")
                    f.write(f"  url:   {driver.current_url}\n")
                    f.write(f"  title: {driver.title}\n\n")
            except Exception:
                pass


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
    login_page.open().login(USERS["standard"], PASSWORD)
    login_page.wait_for_inventory_redirect()
    inventory_page.wait_until_loaded()
    return inventory_page
