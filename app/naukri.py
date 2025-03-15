from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime
import requests
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from shared.login import naukriLogIN
from dotenv import load_dotenv
load_dotenv()
import logging
logger = logging.getLogger()

class naukriAutomation():
    def __init__(self):
        pass
    
    async def updateResume(self, userName, password):
        try:
            service = Service(GeckoDriverManager().install())

            # Configure Firefox options
            options = webdriver.FirefoxOptions()
            options.add_argument('--disable-notifications')
            # options.add_argument('--headless')  # Run Firefox in headless mode (without opening browser window)
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel,application/x-msexcel,application/x-excel,application/excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/csv,application/csv,application/excel,application/vnd.msexcel,text/comma-separated-values,text/x-comma-separated-values,application/octet-stream")
            options.set_preference("browser.helperApps.alwaysAsk.force", False)
            options.set_preference("network.proxy.type", 0)  # Direct connection (no proxy)
            options.set_preference("network.http.use-cache", False)  # Disable caching
            options.set_preference("permissions.default.image", 2)  # Disable loading images
            options.set_preference("dom.webdriver.enabled", False)  # Prevent detection as bot

            driver = webdriver.Firefox(service=service, options=options)
            login = naukriLogIN(driver=driver)
            login_status = login.login(userName=userName, password=password)
            if not login_status:
                return False
            return True
        except Exception as e:
            logger.error(f"UPDATE : Error in Main : {e}")
            return False