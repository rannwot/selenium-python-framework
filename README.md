# Selenium + Python Automation Framework

A production-style test automation framework using **Page Object Model (POM)**, **pytest**, and **SauceDemo** as the target application.

## Features

- **Page Object Model** — maintainable, reusable page classes
- **Test coverage** — login, product search/sort, checkout flows
- **Dual reporting** — pytest-html + Allure
- **CI/CD** — GitHub Actions runs tests headlessly on every push

## Project Structure

```
├── .github/workflows/ci.yml   # GitHub Actions pipeline
├── pages/                     # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── conftest.py            # Fixtures (driver, logged-in session)
│   ├── test_login.py
│   ├── test_search.py
│   └── test_checkout.py
├── utils/config.py            # URLs, credentials, timeouts
├── pytest.ini
└── requirements.txt
```

## Prerequisites

- Python 3.10+
- Google Chrome (installed locally for headed runs)

## Setup

```bash
# macOS: use python3 (there is usually no "python" command)
python3 -m venv venv

source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

If `venv/` already exists (like in this project), skip `python3 -m venv venv` and just activate + install.

## Run Tests

```bash
# Headed (visible browser)
pytest

# Headless
pytest --headless

# Run a specific suite
pytest tests/test_login.py -v
```

Reports are generated automatically:

| Report | Location |
|--------|----------|
| pytest-html | `reports/report.html` |
| Allure raw results | `reports/allure-results/` |

### View Allure Report Locally

```bash
# Install Allure CLI (macOS)
brew install allure

# Generate and open report
allure serve reports/allure-results
```

## Test Suites

| Suite | What it covers |
|-------|----------------|
| `test_login.py` | Valid login, invalid credentials, locked user, empty password |
| `test_search.py` | Sort by name/price, find product and add to cart |
| `test_checkout.py` | Single/multi-item checkout, form validation |

## CI/CD

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on every push and pull request:

1. Installs Python dependencies
2. Runs all tests headlessly with Chrome
3. Uploads pytest-html and Allure reports as artifacts

After a CI run, download reports from the **Actions** tab → select the workflow run → **Artifacts**.

## Why SauceDemo?

[SauceDemo](https://www.saucedemo.com) is a purpose-built demo site for automation practice — stable selectors, no CAPTCHA, and realistic e-commerce flows (login → browse → cart → checkout).

## Next Steps (Portfolio Enhancements)

- Add parallel execution with `pytest-xdist`
- Integrate Allure report publishing via GitHub Pages
- Add API layer tests with `requests`
- Parameterize tests from CSV/JSON data files
- Add visual regression with `pytest-playwright` or Percy
