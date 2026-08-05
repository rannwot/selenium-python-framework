Feature: Checkout
  As a logged-in SauceDemo customer
  I want to add products to my cart and complete checkout
  So that I can purchase items successfully

  Background:
    Given I am logged in as the "standard" user
    And I am on the inventory page

  @critical
  Scenario: Complete checkout with a single item
    When I add "Sauce Labs Backpack" to the cart
    And I go to the cart
    Then the cart should contain 1 item
    When I proceed to checkout
    And I fill in shipping details with first name "Jane", last name "Doe", and postal code "90210"
    Then the checkout overview title should be "Checkout: Overview"
    And the subtotal should be greater than 0
    When I finish the order
    Then I should see the completion message "Thank you for your order!"

  Scenario: Complete checkout with multiple items
    When I add the following products to the cart:
      | product                     |
      | Sauce Labs Backpack         |
      | Sauce Labs Bike Light       |
      | Sauce Labs Bolt T-Shirt     |
    Then the cart badge should show 3 items
    When I go to the cart
    Then the cart should contain 3 items
    When I proceed to checkout
    And I fill in shipping details with first name "John", last name "Smith", and postal code "10001"
    And I finish the order
    Then I should see a completion message containing "Thank you"

  Scenario Outline: Checkout fails when a required shipping field is missing
    When I add "Sauce Labs Backpack" to the cart
    And I go to the cart
    And I proceed to checkout
    And I fill in shipping details with first name "<first_name>", last name "<last_name>", and postal code "<postal_code>"
    Then an error message should be displayed
    And the error message should mention "required"

    Examples:
      | first_name | last_name | postal_code |
      |             | Doe       | 90210       |
      | Jane        |           | 90210       |
      | Jane        | Doe       |             |
