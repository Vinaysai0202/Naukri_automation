import logging
logger = logging.getLogger()

class naukriLogIN():
    def __init__(self,driver):
        self.driver = driver

    async def login(self, userName, password):
            
        try:
            # service = Service(ChromeDriverManager().install())
            # options = webdriver.ChromeOptions()
            # options.add_argument('--disable-notifications')
            # options.add_argument('--headless')
            # options.add_argument('--no-sandbox')
            # options.add_argument('--disable-dev-shm-usage')
            # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

            # driver = webdriver.Chrome(service=service, options=options)

            
            # Navigate to the login page
            self.driver.get("https://www.naukri.com/nlogin/login")

            # Find the username and password input fields and submit button
            username_input = self.driver.find_element("name", "userNameForLogin")
            password_input = self.driver.find_element("name", "passwordForLogin")
            submit_button = self.driver.find_element("css selector", "input[type=submit]")

            # Enter username and password
            username_input.send_keys(userName)
            password_input.send_keys(password)

            # Click the submit button to log in
            submit_button.click()

            return True
        except Exception as e:
            logger.error(f"LOGIN : Error occurred : {e}")
            return None