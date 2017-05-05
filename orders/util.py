from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
import time
import decimal
import os
from .models import Order
from django.shortcuts import get_object_or_404


USER_AGENT = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) " \
             "Chrome/57.0.2987.133 Safari/537.36"


def generate_order_id():
    temp = [str(random.randrange(10)) for i in range(10)]
    return ''.join(temp)


def get_payment_log(order_id):
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = USER_AGENT
    dcap["phantomjs.page.settings.loadImages"] = False
    driver = webdriver.PhantomJS(desired_capabilities=dcap)

    driver.get('https://www.alipay.com')
    print('进入支付宝')
    time.sleep(3)
    if '进入我的支付宝' in driver.page_source:
        driver.find_element_by_xpath('//*[@id="J_mainMenu"]/dl/dd/a').click()
    else:
        driver.find_element_by_class_name('personal-login').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="J_videoContainer"]/div[2]/div/div[2]/a[1]').click()
        time.sleep(1)
        driver.switch_to.frame('J_loginIframe')
        driver.find_element_by_id('J-input-user').send_keys('13750056564')
        time.sleep(1)
        driver.find_element_by_id('password_rsainput').send_keys(os.environ['paypw'])
        time.sleep(1)
        driver.find_element_by_id('J-login-btn').click()
    print('完成登录')
    time.sleep(5)
    driver.execute_script('window.stop()')
    # print(browser.page_source.decode('gbk').encode('utf8'))
    if '账户余额' in driver.page_source:
        # cookies = browser.get_cookies()
        # tmp_list = [dic['name'] + '=' + dic['value'] for dic in cookies]
        # cookie_str = '; '.join(tmp_list)
        # success,message = True, cookie_str
        driver.get('https://consumeprod.alipay.com/record/standard.htm')
        print('已转至订单页面')
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="topSearchForm"]/div[2]/div[2]/a').click()
        time.sleep(1)
        driver.find_element_by_id('J-keyword').click()
        time.sleep(1)
        driver.find_element_by_id('J-keyword').send_keys(order_id)
        time.sleep(1)
        driver.find_element_by_id('J-keyword-btn').click()
        print('已完成查询')
        time.sleep(1)
        if '没有找到记录' in driver.page_source:
            success, message = True, '没有相应的支付记录'
        else:
            pay_amount = driver.find_element_by_class_name('amount-pay').text
            # pay_amount = decimal.Decimal(pay_amount.replace(' ', ''))
            success, message = True, pay_amount
    # elif '验证码' in browser.page_source and '短信' in browser.page_source:
    #     return False, '需要手机验证码，登录失败'
    else:
        success, message = False, '登录失败'

    driver.quit()
    return success, message


def change_payment_status(order_id):
    success = False
    payment_message = ''
    print('开始获取订单%s的支付状态' % order_id)
    while not success:
        success, payment_message = get_payment_log(order_id)
    if payment_message == '没有相应的支付记录':
        return '您的订单还未支付'
    else:
        order = get_object_or_404(Order, id=order_id)
        if order.status == 1:
            order.status = 2
            order.save()
        return '您的订单已经支付 ¥%s' % payment_message
