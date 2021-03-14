import os
from selenium import webdriver


current_path = os.path.dirname(os.path.realpath(__file__))

class Base:
    def __init__(self, driver_path=f'{current_path}/drivers/chromedriver'):
        self.driver_path = driver_path
        self.headers = {}
        self.position = (0,0)
        self.size = (1000,1000)

    def print(self, info=''):
        info = f'[ {self.__class__.__name__} ] {info}'
        print(info)

    def __init_driver(self):
        driver=webdriver.Chrome(self.driver_path)
        driver.set_window_position(*self.position)
        driver.set_window_size(*self.size)
        return driver

    def get_interceptor(self, headers):
        def interceptor(request):
            for k,v in headers.items():
                request.headers[k] = v
        return interceptor

    def get_driver(self):
        driver = self.__init_driver()
        if self.headers:
            driver.request_interceptor = self.get_interceptor(self.headers)
        return driver

    def click_button(self, driver, position, method='xpath'):
        if method=='xpath':
            driver.find_element_by_xpath(position).click()
        elif method=='css_selector':
            driver.find_element_by_css_selector(position).click()

    def scroll_to_bottom(self, driver):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
