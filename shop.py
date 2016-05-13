# coding=utf-8

###--------------------------------------------------
###@author		ZhangYucai<zhangyucai@foxmail.com>
###@copyright	2016ZhangYucai
###@version1.0.0
###@since		2016-5-12
###@doc			积分商城 speed
###--------------------------------------------------
import requests
import sys
import bs4
import sys

LOGIN_URL = "http:"
SHOP_URL = 'http:'
BUY_URL = 'http:'
class Shop(object):
    def __init__(self, username, password):
        self.session = requests.session()
        self.post_data = {'username': user, 'passwd': password}
        self.hc = ""

    def login(self):
        self.session.post(LOGIN_URL, data = self.post_data)

    def get_md5(self):
        r = self.session.get(SHOP_URL)
        r.encoding=r.apparent_encoding
        soup = bs4.BeautifulSoup(r.text, "lxml")

        jss = soup.find_all('script')
        js = jss[len(jss)-1]
        js=js.text
        begin = js.find('}();')
        end = js.find('app.qiandao(')

        targetjs = js[begin+4: end]
        targetjs = targetjs.lstrip().replace(';', '\n') #clear semicolon
        targetjs = targetjs.replace('var', '') #clear var
        targetjs = targetjs.replace(' ', '') # clear space
        targetjs = targetjs.replace('	', '') # clear tab
        
        exec(targetjs)

        targetend = js.find(')', end+1)
        val = js[end+12: targetend]
        self.hc = eval(val) 

    def buy(self, shopid, number):
        post_data = {'id': shopid, 'des': "", 'number': number, 'hc': self.hc}
        r = self.session.post(BUY_URL, data = post_data)
        print r.text


    def show_md5(self):
    	print self.hc
    


if __name__ == '__main__':
    user = 'username'
    password = 'pass'
    shop = Shop(user, password)
    shop.login()
    shop.get_md5()
    #shop.show_md5()
    shop.buy(269, 2) #e card
    shop.buy(267, 2) #jd card
    shop.buy(277, 1) #a bo