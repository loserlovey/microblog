#coding=utf-8
from selenium import webdriver
from config import myconfig
from time import sleep

def process_wahuasuan():
    # wahuasuan.com, QQ
    url = "http://www.wahuasuan.com/?m=user&a=login"
    id_field_name = "pop_username"
    passwd_field_name = "pop_password"
    btn_field_name = "pop-btn-login"
    my_id = myconfig['wahuasuan_id']
    my_password = myconfig['wahuasuan_pwd']
    browser = webdriver.Firefox()
    browser.get(url)
    browser.find_element_by_id(id_field_name).clear()
    browser.find_element_by_id(id_field_name).send_keys(my_id)
    browser.find_element_by_id(passwd_field_name).clear()
    browser.find_element_by_id(passwd_field_name).send_keys(my_password)
    browser.find_element_by_id(btn_field_name).click()
    browser.find_element_by_class_name("sign").click()
    print('wahuasuan finished...')
    browser.quit()

def process_jd():
    # jd.com
    passporturl = 'https://passport.jd.com/uc/login?ReturnUrl=http%3A%2F%2Fvip.jd.com%2Fhome.html'
    jd_id = myconfig['jd_id']
    jd_passwd = myconfig['jd_pwd']
    checked_field_class_name = 'checked'
    user_field_id = 'loginname'
    password_field_id = 'nloginpwd'
    btn_field_id = 'loginsubmit'
    browser = webdriver.Firefox()
    browser.get(passporturl)
    
    try:
        browser.find_element_by_link_text(u'账户登录').click()
        browser.find_element_by_id(user_field_id).clear()
        browser.find_element_by_id(user_field_id).send_keys(jd_id)
        browser.find_element_by_id(password_field_id).clear()
        browser.find_element_by_id(password_field_id).send_keys(jd_passwd)
        browser.find_element_by_id(btn_field_id).click()
        browser.find_element_by_class_name("icon-sign").click()
    except:
        pass

    sleep(10)
    passporturl = "https://passport.jd.com/new/login.aspx?ReturnUrl=http%3A%2F%2Fvip.jr.jd.com%2F"
    browser.get(passporturl)

    try:
        browser.find_element_by_link_text(u'账户登录').click()
        browser.find_element_by_id(user_field_id).clear()
        browser.find_element_by_id(user_field_id).send_keys(jd_id)
        browser.find_element_by_id(password_field_id).clear()
        browser.find_element_by_id(password_field_id).send_keys(jd_passwd)
        browser.find_element_by_id(btn_field_id).click()
        browser.find_element_by_class_name("qian-text").click()
    except:
        pass

    browser.quit()
    
    # passporturl = "https://passport.jd.com/new/login.aspx?ReturnUrl=http%3A%2F%2Fyou.jd.com%2Fchannel%2Fshouji.html"
    # browser = webdriver.Firefox()
    # browser.get(passporturl)
    # browser.find_element_by_link_text(u'账户登录').click()
    # browser.find_element_by_id(user_field_id).send_keys(jd_id)
    # browser.find_element_by_id(password_field_id).send_keys(jd_passwd)
    # browser.find_element_by_id(btn_field_id).click()
    # browser.find_element_by_class_name("icon-sprite").click()

    print(u'jd finished...')

if __name__ == '__main__':
    process_wahuasuan()
    process_jd()