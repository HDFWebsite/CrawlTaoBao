#coding=utf-8
import time,random,requests,json

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class Taobao(object):

    def __init__(self,name,password):
        self.name=name
        self.password=password
        self.login_url='https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fwww.taobao.com%2F'
        self.order_url='https://buyertrade.taobao.com/trade/itemlist/asyncBought.htm?action=itemlist/BoughtQueryAction&event_submit_do_query=1&_input_charset=utf8'
        self.num=0
        self.cost=0

    def login(self):
        driver=webdriver.Chrome('C:\\Users\\Administrator\\Downloads\\chromedriver.exe')
        driver.get(self.login_url)
        driver.find_element_by_id('J_Quick2Static').click()
        WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.ID, 'TPL_username_1')))
        driver.find_element_by_id('TPL_username_1').send_keys(self.name)
        driver.save_screenshot('1.jpg')   ##用phantomjs无界面浏览器最好需要截图
        driver.find_element_by_id('TPL_password_1').send_keys(self.password)
        driver.save_screenshot('2.jpg')
        driver.find_element_by_id('J_SubmitStatic').click()
        time.sleep(10)
        driver.save_screenshot('1.jpg')
        self.cookies={}
        for dictx in driver.get_cookies():
            self.cookies[dictx['name']]=dictx['value']
        driver.quit()


    def get_orders(self,p,flag):
        if flag==0:
            self.login()
            print('self.cookies')
        datax={'pageNum':p+1,
                'pageSize':15,
               'prePageNo':p,
               }
        header = {'origin': 'https://buyertrade.taobao.com',  ###origin和refere一定需要，否则会请求不到订单数据
                'referer':'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                  #'cookie':'miid=387872062667523128; thw=cn;xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.....',  ##如果不用浏览器登录，可以在headrs中携带字符串形式的cookie
                  }
        resp=requests.post(self.order_url,data=datax,cookies=self.cookies,headers=header)
        #resp=requests.post(self.order_url,data=datax,headers=header)
        #print resp.content.decode('gbk')
        orders_dictx = json.loads(resp.content.decode('gbk'))
        pages=orders_dictx['page']['totalPage']
        for order in orders_dictx['mainOrders']:
            self.num+=1

            self.cost+=float(order['payInfo']['actualFee'])
            print("self.num,' ',order['subOrders'][0]['itemInfo']['title'],'价格是： ',order['payInfo']['actualFee'],'元 交易状态是：',order['statusInfo']['text'],self.cost")

        if flag==0:
            for p in range(1,pages+1):
                self.get_orders(p,1)

if __name__=="__main__":
    pass
    tb=Taobao('登录账号','登录密码')
    tb.get_orders(0,0)