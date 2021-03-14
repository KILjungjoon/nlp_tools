try:
    from .base import Base
except:
    from base import Base

from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import parse_qs
import urllib.parse as urlparse
import pandas as pd
import time
import re

class GooglePlay(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = None
        self.scroll_cnt = 50
        self.result_file = './result.csv'

        self.bs4_parser = 'html.parser'

        self.target_columns = ['name', 'ratings', 'date', 'helpful', 'comment', 'developer_comment']

    def scroll_to_load_data(self, driver):
        self.scroll_to_bottom(driver)
        time.sleep(3)
        try:
            # bottom xpath
            xpath = "/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/div[2]/div[2]/div/span/span"
            self.click_button(driver, xpath, 'xpath')
            self.print('Clicked button.')
        except:
            self.print('Loading...')

    def get_star(self, s):
        stars = re.findall(r'[-+]?\d*\.\d+|\d+', s)
        stars.sort()
        return int(stars[0])

    def get_language(self):
        parsed = urlparse.urlparse(self.url)
        return parse_qs(parsed.query)['hl'][0].lower()

    def get_datatime_format(self):
        datetime_format = {
            'ko': '%Y년 %m월 %d일',
            'en': '%B %d, %Y',
            'cn': '%Y年%m月%d日',
            'ja': '%Y年%m月%d日',
        }
        lang = self.get_language()
        return datetime_format[lang] if lang in datetime_format else None

    def get_date(self, s):
        date = datetime.strptime(s, self.get_datatime_format())
        return date.strftime('%Y-%m-%d')

    def parse_xml(self, xml):
        # parse string to html using bs4
        soup = BeautifulSoup(xml, self.bs4_parser)

        data = {column:None for column in self.target_columns}
        data['name']    = soup.find(class_='X43Kjb').text  # reviewer
        data['ratings'] = self.get_star(soup.find('div', role='img').get('aria-label'))  # rating
        data['date']    = self.get_date(soup.find(class_='p2TkOb').text)  # review date

        helpful = soup.find(class_='jUL89d y92BAb').text
        data['helpful'] = helpful if helpful else 0  # helpful

        comment = soup.find('span', jsname='fbQN7e').text
        data['comment'] = comment if comment else soup.find('span', jsname='bN97Pc').text  # review text

        dc_div = soup.find('div', class_='LVQB0b')
        data['developer_comment'] = dc_div.text.replace('\n', ' ') if dc_div else None  # developer comment

        return data

    def run_script(self):
        driver = self.get_driver()
        driver.get(self.url)
        scroll_cnt  = self.scroll_cnt
        result_file = self.result_file

        for i in range(scroll_cnt):
            self.scroll_to_load_data(driver)

        reviews = driver.find_elements_by_xpath('//*[@jsname="fk8dgd"]//div[@class="d15Mdf bAhLNe"]')
        self.print(f'There are {len(reviews)} reviews avaliable!')
        self.print('Writing the data...')

        df = pd.DataFrame(columns=self.target_columns)

        for review in reviews:
            data = self.parse_xml(review.get_attribute('innerHTML'))
            # append to dataframe
            df = df.append(data, ignore_index=True)

        # finally save the dataframe into csv file
        filename = datetime.now().strftime('result/%Y-%m-%d_%H-%M-%S.csv')
        df.to_csv(result_file, encoding='utf-8-sig', index=False)
        driver.stop_client()
        driver.close()
        self.print('Finished.')


if __name__ == '__main__':
    gp             = GooglePlay()
    gp.url         = 'https://play.google.com/store/apps/details?id=com.supercell.brawlstars&showAllReviews=true&hl=ja'
    gp.result_file = './result.csv'
    gp.scroll_cnt  = 1
    gp.headers     = {'accept-language': 'ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7'}
    gp.run_script()
