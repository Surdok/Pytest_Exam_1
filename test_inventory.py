"""
Exam 1 - Test Inventory Module
================================
Write your tests below. Each section (Part A through E) is marked.
Follow the instructions in each part carefully.

Run your tests with:
    pytest test_inventory.py -v

Run with coverage:
    pytest test_inventory.py --cov=inventory --cov-report=term-missing -v
"""

import pytest
from unittest.mock import patch
from inventory import (
    add_product,
    get_product,
    update_stock,
    calculate_total,
    apply_bulk_discount,
    list_products,
)


# ============================================================
# FIXTURE: Temporary inventory file (provided for you)
# This ensures each test gets a clean, isolated inventory.
# ============================================================

@pytest.fixture(autouse=True)
def clean_inventory(tmp_path, monkeypatch):
    """Use a temporary inventory file for each test."""
    db_file = str(tmp_path / "inventory.json")
    monkeypatch.setattr("inventory.INVENTORY_FILE", db_file)
    yield


# ============================================================
# PART A - Basic Assertions (18 marks)
# Write at least 8 tests using plain assert statements.
# Cover: add_product, get_product, update_stock,
#        calculate_total, and list_products.
# Follow the AAA pattern (Arrange, Act, Assert).
# ============================================================

# TODO: Write your Part A tests here

# add_product
def test_add_product_valid():
    # Arrange
    product_id = "123"
    name = "Product 1"
    price = 10.0
    stock = 100
    # Act
    add_product(product_id, name, price, stock)
    # Assert
    assert get_product(product_id) == {
        "product_id": product_id, "name": name, "price": price, "stock": stock}


def test_add_product_invalid_product_id():
    # Arrange
    product_id = ""
    name = "Product 1"
    price = -10.0  # negative price
    stock = 100
    # Act
    with pytest.raises(ValueError):
        add_product(product_id, name, price, stock)
    # Assert
    assert get_product(product_id) is None


def test_get_product_valid():
    # Arrange
    product_id = "123"
    name = "Product 1"
    price = 10.0
    stock = 100
    add_product(product_id, name, price, stock)
    # Act
    assert get_product(product_id) == {
        "product_id": product_id, "name": name, "price": price, "stock": stock}


def test_get_product_invalid():
    # Arrange
    product_id = "123"
    # Act
    product = get_product(product_id)
    # Assert
    assert product is None


def test_update_stock_valid():
    # Arrange
    product_id = "123"
    name = "Product 1"
    price = 10.0
    stock = 100
    # Act
    add_product(product_id, name, price, stock)
    update_stock(product_id, 10)
    # Assert
    assert get_product(product_id) == {
        "product_id": product_id, "name": name, "price": price, "stock": stock + 10}


def test_update_stock_invalid():
    # Arrange
    product_id = "123"
    name = "Product 1"
    price = 10.0
    stock = 2
    # Act
    add_product(product_id, name, price, stock)
    with pytest.raises(ValueError):
        update_stock(product_id, -10)
    # Assert
    assert get_product(product_id) == {
        "product_id": product_id, "name": name, "price": price, "stock": stock}


def test_calculate_total_valid():
    # Arrange
    product_id = "123"
    name = "Product 1"
    price = 10.0
    stock = 100
    # Act
    add_product(product_id, name, price, stock)
    # Assert
    assert calculate_total(product_id, 10) == 100


def test_calculate_total_invalid():
    # Arrange
    product_id = "123"
    name = "Product 1"
    price = 10.0
    stock = 100
    # Act
    add_product(product_id, name, price, stock)
    with pytest.raises(ValueError):
        calculate_total(product_id, -10)
    # Assert
    assert get_product(product_id) == {
        "product_id": product_id, "name": name, "price": price, "stock": stock}


def test_list_products_valid():
    # Arrange
    product_id = "123"
    name = "Product 1"
    price = 10.0
    stock = 100
    # Act
    add_product(product_id, name, price, stock)
    # Assert
    assert list_products() == [
        {"product_id": product_id, "name": name, "price": price, "stock": stock}]
# ============================================================
# PART B - Exception Testing (12 marks)
# Write at least 6 tests using pytest.raises.
# add_product with empty product_id → ValueError
# add_product with empty name → ValueError
# add_product with negative price → ValueError
# add_product with duplicate product_id → ValueError
# update_stock that would make stock negative → ValueError
# calculate_total with quantity <= 0 → ValueError
# Tip: Use the match parameter to verify the error message, e.g.: pytest.raises(ValueError, match="Price must be positive")

# ============================================================

# TODO: Write your Part B tests here


def test_add_product_empty_product_id():
    # Arrange
    product_id = ""
    name = "Product 1"
    price = 10.0
    stock = 100
    # Act
    with pytest.raises(ValueError, match="Product ID and name are required"):
        add_product(product_id, name, price, stock)
    # Assert
    assert get_product(product_id) is None


def test_add_product_empty_name():
    # Arrange
    product_id = "123"
    name = ""
    price = 10.0
    stock = 100
    # Act
    with pytest.raises(ValueError, match="Product ID and name are required"):
        add_product(product_id, name, price, stock)
    # Assert
    assert get_product(product_id) is None


def test_add_product_negative_price():
    # Arrange
    product_id = "123"
    name = "Product 1"
    price = -10.0
    stock = 100
    # Act
    with pytest.raises(ValueError, match="Price must be positive"):
        add_product(product_id, name, price, stock)
    # Assert
    assert get_product(product_id) is None


def test_add_product_duplicate_product_id():
    # Arrange
    product_id = "123"
    name = "Product 1"
    price = 10.0
    stock = 100
    # Act
    add_product(product_id, name, price, stock)
    # Assert
    with pytest.raises(ValueError, match="Product '123' already exists"):
        add_product(product_id, name, price, stock)


def test_update_stock_negative_stock():
    # Arrange
    product_id = "123"
    name = "Product 1"
    price = 10.0
    stock = 100
    # Act
    add_product(product_id, name, price, stock)
    # Assert
    with pytest.raises(ValueError, match="Stock cannot go below zero"):
        update_stock(product_id, -110)


def test_calculate_total_negative_quantity():
    # Arrange
    product_id = "123"
    name = "Product 1"
    price = 10.0
    stock = 100
    # Act
    add_product(product_id, name, price, stock)
    # Assert
    with pytest.raises(ValueError, match="Quantity must be positive"):
        calculate_total(product_id, -10)

# ============================================================
# PART C - Fixtures and Parametrize (10 marks)
#
# C1:

# Create a @pytest.fixture called sample_products that:
# Adds 3 products to inventory
# (e.g. "P001" Laptop $999.99 stock 10, "P002" Mouse $29.99 stock 50, "P003" Keyboard $79.99 stock 25)
# Returns a list of the 3 product IDs: ["P001", "P002", "P003"]
# Then write 2 tests that use this fixture. For example, test that list_products returns 3 items, or test that calculate_total works for one of the sample products.


# TODO: Write your Part C tests here


@pytest.fixture
def sample_products():
    product_id_1 = "P001"
    product_id_2 = "P002"
    product_id_3 = "P003"
    add_product(product_id_1, "Laptop", 999.99, 10)
    add_product(product_id_2, "Mouse", 29.99, 50)
    add_product(product_id_3, "Keyboard", 79.99, 25)
    return list_products()


def test_list_products_with_sample_products(sample_products):

    assert len(sample_products) == 3


def test_calculate_total_with_sample_products(sample_products):
    assert calculate_total(sample_products[0]['product_id'], 10) == 999.99 * 10

# Use @pytest.mark.parametrize to test apply_bulk_discount with at least 5 different input combinations.
# Each row should be (total, quantity, expected_result).
# Remember the discount rules:
# •	Under 10 items → no discount (0%)
# •	10–24 items → 5% off
# •	25–49 items → 10% off
# •	50+ items → 15% off


@pytest.mark.parametrize("total, quantity, expected_result", [
    (500, 5, 500),
    (500, 10, 500 * 0.95),
    (500, 25, 500 * 0.9),
    (500, 49, 500 * 0.9),
    (500, 50, 500 * 0.85),
])
def test_apply_bulk_discount(total, quantity, expected_result):
    assert apply_bulk_discount(total, quantity) == expected_result

# ============================================================
# PART D - Mocking (5 marks)
# Use @patch to mock _send_restock_alert.
# Write 2 tests:
#   1. Verify the alert IS called when stock drops below 5
#   2. Verify the alert is NOT called when stock stays >= 5
# ============================================================

# TODO: Write your Part D tests here


# ============================================================
# PART E - Coverage (5 marks)
# Run: pytest test_inventory.py --cov=inventory --cov-report=term-missing -v
# You must achieve 90%+ coverage on inventory.py.
# If lines are missed, add more tests above to cover them.
# ============================================================


# ============================================================
# BONUS (5 extra marks)
# 1. Add a function get_low_stock_products(threshold) to
#    inventory.py that returns all products with stock < threshold.
# 2. Write 3 parametrized tests for it below.
# ============================================================

# TODO: Write your bonus tests here (optional)
