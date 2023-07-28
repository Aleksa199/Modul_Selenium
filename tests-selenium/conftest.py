import pytest
from selenium import webdriver


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.set_headless(True)
    return chrome_options


