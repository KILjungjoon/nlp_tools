from tools import GooglePlay


driver_path = './tools/crawler/drivers/chromedriver'

gp             = GooglePlay(driver_path)
gp.url         = 'https://play.google.com/store/apps/details?id=air.com.speakingmax&hl=ko&showAllReviews=true'
gp.result_file = './sample_crawler_result.csv'
gp.scroll_cnt  = 10
gp.headers     = {'accept-language': 'ko,ko-KR;q=0.9,en-US;q=0.8,en;q=0.7'}
# gp.run_script()
