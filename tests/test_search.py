import allure


@allure.feature("Product Search & Sort")
@allure.story("Inventory filtering")
class TestSearch:
    @allure.title("Sort products by name A to Z")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_name_ascending(self, logged_in_inventory):
        inventory = logged_in_inventory
        inventory.sort_by("name_asc")
        names = inventory.get_product_names()
        assert names == sorted(names)

    @allure.title("Sort products by name Z to A")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_name_descending(self, logged_in_inventory):
        inventory = logged_in_inventory
        inventory.sort_by("name_desc")
        names = inventory.get_product_names()
        assert names == sorted(names, reverse=True)

    @allure.title("Sort products by price low to high")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_price_ascending(self, logged_in_inventory):
        inventory = logged_in_inventory
        inventory.sort_by("price_asc")
        prices = inventory.get_product_prices()
        assert prices == sorted(prices)

    @allure.title("Sort products by price high to low")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_by_price_descending(self, logged_in_inventory):
        inventory = logged_in_inventory
        inventory.sort_by("price_desc")
        prices = inventory.get_product_prices()
        assert prices == sorted(prices, reverse=True)

    @allure.title("Find product by name and add to cart")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_find_product_and_add_to_cart(self, logged_in_inventory, cart_page):
        inventory = logged_in_inventory
        product_name = "Sauce Labs Backpack"
        inventory.add_product_to_cart_by_name(product_name)
        assert inventory.get_cart_item_count() == 1

        inventory.go_to_cart()
        assert cart_page.is_loaded()
        assert product_name in cart_page.get_cart_item_names()
