"""Central configuration for the SauceDemo automation framework."""

import os

BASE_URL = "https://www.saucedemo.com"

# Standard SauceDemo test accounts
USERS = {
    "standard": "standard_user",
    "locked": "locked_out_user",
    "problem": "problem_user",
    "performance": "performance_glitch_user",
}

PASSWORD = "secret_sauce"

DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "10"))
