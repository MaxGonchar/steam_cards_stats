from typing import Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class element_has_non_empty_text(object):
  def __init__(self, locator):
    self.locator = locator

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    print(element)
    if element.text.strip() != '':
        return element
    else:
        return False


class CardPage:
    
    def __enter__(self, timeout: int = 10):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, timeout)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    
    def get(self, url: str) -> Optional[str]:
        print(f"Get content for URL {url}")
        self.driver.get(url)

        try:
            self.wait.until(element_has_non_empty_text((By.ID, 'market_commodity_forsale')))
            self.wait.until(element_has_non_empty_text((By.ID, 'market_commodity_buyrequests')))
            content = self.driver.page_source
            print("Done")
            return content
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Failed to get content for URL {url} \n {str(e)}")
            return
