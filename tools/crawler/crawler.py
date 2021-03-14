import os

import time
import pandas as pd
from bs4 import BeautifulSoup 
from datetime import datetime
from selenium import webdriver


current_path = os.path.dirname(os.path.realpath(__file__))

class Base:
    def __init__(self, driver_path=f'{current_path}/drivers/chromedriver'):
        self.driver_path = driver_path
        self.headers = {}
        self.position = (0,0)
        self.size = (1000,1000)

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


class GooglePlay(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = None
        self.scroll_cnt = 50
        self.result_file = './result.csv'

    def run_script(self):
        driver = self.get_driver()
        driver.get(self.url)
        scroll_cnt  = self.scroll_cnt
        result_file = self.result_file

        for i in range(scroll_cnt):
            self.scroll_to_bottom(driver)
            time.sleep(3)
            try:
                xpath = "/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/div[2]/div/span/span"
                # css_target = '#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div > main > div > div.W4P4ne > div:nth-child(2) > div.PFAhAf > div > span > span'
                self.click_button(driver, xpath, 'xpath')
                print('[ GooglePlay ] Clicked button.')
            except:
                pass

        reviews = driver.find_elements_by_xpath('//*[@jsname="fk8dgd"]//div[@class="d15Mdf bAhLNe"]')
        print(f'[ GooglePlay ] There are {len(reviews)} reviews avaliable!')
        print('[ GooglePlay ] Writing the data...')

        # create empty dataframe to store data
        df = pd.DataFrame(columns=['name', 'ratings', 'date', 'helpful', 'comment', 'developer_comment'])

        # get review data
        for review in reviews:
            # parse string to html using bs4
            soup = BeautifulSoup(review.get_attribute('innerHTML'), 'html.parser')

            # reviewer
            name = soup.find(class_='X43Kjb').text

            # rating
            ratings = int(soup.find('div', role='img').get('aria-label').replace('별표 5개 만점에', '').replace('개를 받았습니다.', '').strip())

            # review date
            date = soup.find(class_='p2TkOb').text
            date = datetime.strptime(date, '%Y년 %m월 %d일')
            date = date.strftime('%Y-%m-%d')

            # helpful
            helpful = soup.find(class_='jUL89d y92BAb').text
            if not helpful:
                helpful = 0

            # review text
            comment = soup.find('span', jsname='fbQN7e').text
            if not comment:
                comment = soup.find('span', jsname='bN97Pc').text

            # developer comment
            developer_comment = None
            dc_div = soup.find('div', class_='LVQB0b')
            if dc_div:
                developer_comment = dc_div.text.replace('\n', ' ')

            # append to dataframe
            df = df.append({
                'name': name,
                'ratings': ratings,
                'date': date,
                'helpful': helpful,
                'comment': comment,
                'developer_comment': developer_comment
            }, ignore_index=True)

        # finally save the dataframe into csv file
        filename = datetime.now().strftime('result/%Y-%m-%d_%H-%M-%S.csv')
        df.to_csv(result_file, encoding='utf-8-sig', index=False)
        driver.stop_client()
        driver.close()
        print('[ GooglePlay ] Finished.')


if __name__ == '__main__':
    gp             = GooglePlay()
    gp.url         = 'https://play.google.com/store/apps/details?id=air.com.speakingmax&hl=ko&showAllReviews=true'
    gp.result_file = './result.csv'
    gp.scroll_cnt  = 10
    gp.headers     = {'accept-language': 'ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7'}
    gp.run_script()
