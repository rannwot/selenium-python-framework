import allure
import pytest


@allure.feature("Checkout")
@allure.story("End-to-end purchase flow")
class TestCheckout:
    @allure.title("Complete checkout with a single item")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_single_item_checkout(
        self, logged_in_inventory, cart_page, checkout_page
    ):
        logged_in_inventory.add_product_to_cart_by_index(0)
        logged_in_inventory.go_to_cart()

        assert cart_page.is_loaded()
        assert cart_page.get_cart_item_count() == 1
        cart_page.proceed_to_checkout()

        checkout_page.fill_shipping_info("Jane", "Doe", "90210")
        assert checkout_page.get_overview_title() == "Checkout: Overview"
        assert checkout_page.get_subtotal() > 0

        checkout_page.finish_order()
        assert checkout_page.get_completion_message() == "Thank you for your order!"

    @allure.title("Checkout with multiple items calculates correct cart count")
    @allure.severity(allure.severity_level.NORMAL)
    def test_multi_item_checkout(self, logged_in_inventory, cart_page, checkout_page):
        inventory = logged_in_inventory
        products = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt",
        ]
        for product in products:
            inventory.add_product_to_cart_by_name(product)

        assert inventory.get_cart_item_count() == 3
        inventory.go_to_cart()

        assert cart_page.get_cart_item_count() == 3
        cart_page.proceed_to_checkout()

        checkout_page.fill_shipping_info("John", "Smith", "10001")
        checkout_page.finish_order()
        assert "Thank you" in checkout_page.get_completion_message()

    @allure.title("Checkout fails when required fields are missing")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "first_name,last_name,postal_code",
        [
            ("", "Doe", "90210"),
            ("Jane", "", "90210"),
            ("Jane", "Doe", ""),
        ],
    )
    def test_checkout_validation(
        self,
        logged_in_inventory,
        cart_page,
        checkout_page,
        first_name,
        last_name,
        postal_code,
    ):
        logged_in_inventory.add_product_to_cart_by_index(0)
        logged_in_inventory.go_to_cart()
        cart_page.proceed_to_checkout()

        checkout_page.fill_shipping_info(first_name, last_name, postal_code)
        assert checkout_page.is_error_displayed()
        assert "required" in checkout_page.get_error_message().lower()
