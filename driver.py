from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from settings import USER_AGENT


def get_driver():
    options = webdriver.EdgeOptions()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument(f"user-agent={USER_AGENT}")

    return webdriver.Edge(
        service=EdgeService(EdgeChromiumDriverManager().install()), options=options
    )
