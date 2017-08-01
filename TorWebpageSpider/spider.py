# -*- encoding:utf8 -*-
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.common.action_chains import ActionChains
from urllib import quote
import urllib2
import urllib
import time
from urllib import urlencode
import swagger_client
from swagger_client.rest import ApiException
from com.aliyun.api.gateway.sdk.util import showapi
import json
import string


#Firefox浏览器配置
profile = webdriver.FirefoxProfile()
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9150)
profile.set_preference('network.proxy.socks_remote_dns',True)
profile.update_preferences()
driver = webdriver.Firefox(profile)

# 识别验证码
def request1(appkey, img_base64,m="GET"):
    url = "http://op.juhe.cn/vercode/index"
    params = {
        "key": appkey,  # 您申请到的APPKEY
        "codeType": "1008",
    # 验证码的类型，&lt;a href=&quot;http://www.juhe.cn/docs/api/id/60/aid/352&quot; target=&quot;_blank&quot;&gt;查询&lt;/a&gt;
        "base64Str": img_base64,  # 图片文件
        "dtype": "json",  # 返回的数据的格式，json或xml，默认为json

    }
    params = urlencode(params)
    if m == "GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)

    content = f.read()

    print "content = " ,content.split("\n")[1]

    res = json.loads(content.split("\n")[1])
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print res["result"]
            return res["result"]
        else:
            print "%s:%s" % (res["error_code"], res["reason"])
    else:
        print "request api error"

def request2(appcode, img_base64,m="POST"):
    url = "http://ali-checkcode2.showapi.com/checkcode"
    params = {
        "key": appcode,  # 您申请到的APPKEY
        "codeType": "1008",
    # 验证码的类型，&lt;a href=&quot;http://www.juhe.cn/docs/api/id/60/aid/352&quot; target=&quot;_blank&quot;&gt;查询&lt;/a&gt;
        "base64Str": img_base64,  # 图片文件
        "dtype": "json",  # 返回的数据的格式，json或xml，默认为json

    }
    params = urlencode(params)
    if m == "GET":
        f = urllib.urlopen("%s?%s" % (url, params))
    else:
        f = urllib.urlopen(url, params)

    content = f.read()

    print "content = " ,content.split("\n")[1]

    res = json.loads(content.split("\n")[1])
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            # 成功请求
            print res["result"]
            return res["result"]
        else:
            print "%s:%s" % (res["error_code"], res["reason"])
    else:
        print "request api error"

def AliAPI(base64,appcode):
    req = showapi.ShowapiRequest( "http://ali-checkcode2.showapi.com/checkcode",appcode )
    json_res= req.addTextPara("typeId","38")\
        .addTextPara("img_base64",base64)\
        .addTextPara("convert_to_jpg","1")\
        .post()
    print ('json_res data is:', json_res)
    print json_res
    print json_res
    print 'jsonres[2][0]', json_res['showapi_res_body']['ret_code']
    print 'jsonres[2][1]', json_res['showapi_res_body']['Result']
    return json_res['showapi_res_body']['ret_code'], json_res['showapi_res_body']['Result']

def get_check():
    check = None
    while True:
        try:
            driver.get("https://bridges.torproject.org/bridges?transport=obfs4")
            time.sleep(2)
            # 购买的appcode
            appcode = 'ad616df07c494fefaa08f1ddffaed204'
            rescode,check = AliAPI(driver.find_element_by_tag_name("img").get_attribute("src")[23:],appcode)
            driver.save_screenshot("screen.jpg")
            api_instance = swagger_client.DefaultApi()
            # result = json.loads(result)
            # check = result['result']['showapi_res_body']['Result']
            if (rescode!=0):
                print "验证码解析错误 code = ", rescode
                print "check is not right,reload the page..."
                continue
            else :
                break
        except WebDriverException:
            print "Script error :",WebDriverException
            continue
    print "will return check:",check
    return check

while True:
    check = get_check()
    print "get check is:",check
    inputarea = driver.find_element_by_id("captcha_response_field")
    button = driver.find_element_by_id("captcha-submit-button")
    action = ActionChains(driver)
    action.move_to_element(inputarea)
    action.click()
    print check[0],check[1],check[2],check[3],check[4],check[5],check[6],check[7]
    action.send_keys(Keys.LEFT_SHIFT)
    action.send_keys(check.__str__())
    action.perform()
    action.move_to_element(button)
    action.click()
    action.perform()

    driver.save_screenshot("screen1.jpg")
    time.sleep(15)
    try:
        bridges = driver.find_elements_by_id("bridgelines")
        print len(bridges)
        if len(bridges) != 0:
            print bridges[0].text.split("\n")
            break
    except exceptions.NoSuchElementException:
        print "check is wrong , reload page"
        continue

# driver.close()


