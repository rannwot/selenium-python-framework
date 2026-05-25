import allure
import pytest

from utils.config import PASSWORD, USERS


@allure.feature("Login")
@allure.story("Authentication")
class TestLogin:
    @allure.title("Standard user can log in successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self, login_page, inventory_page):
        login_page.open().login(USERS["standard"], PASSWORD)
        login_page.wait_for_inventory_redirect()
        inventory_page.wait_until_loaded()
        assert "Sauce Labs Backpack" in inventory_page.get_product_names()

    @allure.title("Invalid credentials show an error message")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_login(self, login_page):
        login_page.open().login("invalid_user", "wrong_password")
        assert login_page.is_error_displayed()
        assert "do not match" in login_page.get_error_message()

    @allure.title("Locked out user cannot log in")
    @allure.severity(allure.severity_level.NORMAL)
    def test_locked_out_user(self, login_page):
        login_page.open().login(USERS["locked"], PASSWORD)
        assert login_page.is_error_displayed()
        assert "locked out" in login_page.get_error_message().lower()

    @allure.title("Login fails when password is empty")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.parametrize("username", [USERS["standard"], ""])
    def test_empty_password(self, login_page, username):
        login_page.open().login(username, "")
        assert login_page.is_error_displayed()
