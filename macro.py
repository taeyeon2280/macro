from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time

id = 'happine2s'
pwd = 'psy3813!'
driver = webdriver.Chrome('C:\\Users\\user\\Desktop\\chromedriver.exe')#바꿀까??ㅇ 실행?ㅇㅇ
main = "https://ticket.interpark.com/Gate/TPLogin.asp?CPage=B&MN=Y&tid1=main_gnb&tid2=right_top&tid3=login&tid4=login"
musical = "http://ticket.interpark.com/Ticket/Goods/GoodsInfo.asp?GoodsCode=20001033"


def login():
    time.sleep(1)
    driver.get(main)
    driver.switch_to.frame(driver.find_element_by_tag_name('iframe'))
    driver.find_element_by_id('userId').send_keys(id)
    driver.find_element_by_id('userPwd').send_keys(pwd)
    driver.find_element_by_id("btn_login").click()


def to_page():
    time.sleep(0.5)
    # 넘어가지 않으면 시간 늘리기
    driver.get(musical)  #창사 뭐시기 페이지 들어옴
    driver.execute_script('javascript:fnNormalBooking();') #예매하기누르면 뜨는 창 열기

def select_date():
    driver.switch_to.window(driver.window_handles[1]) #로딩 기다리면서 새창 전환
    time.sleep(0.7) #기다리기
    # 동적으로 바꾸기
    iframe = driver.find_element_by_id('ifrmBookStep') #ifrmBookStep:예매창
    #iframe = 다른 html문서에 포함된 html문서에 삽입된 웹페이지
    driver.switch_to.frame(iframe) #예매창으로 전환
    driver.find_element_by_xpath('//*[@id="CellPlayDate"]').click()
    time.sleep(0.7)
    # 동적으로 바꾸기
    driver.switch_to.default_content()
    driver.execute_script("javascript:fnNextStep('P');")
    #javascript:fnNextStep('P') : 다음단계 href

def select_seat():
    # 부모iframe
    while len(driver.find_elements_by_id('ifrmSeat')) == 0:
        pass
    driver.switch_to.frame(driver.find_element_by_id('ifrmSeat'))

    # 자식iframe
    while len(driver.find_elements_by_id('ifrmSeatDetail')) == 0:
        pass
    driver.switch_to.frame(driver.find_element_by_id('ifrmSeatDetail'))

    # 동적으로 바꾸기
    time.sleep(0.7)

    #bs4로 html 파싱하기
    req = driver.page_source #문자열-driver.page_source : 브라우저에 보이는 그대로의 탭내용
    dummy = bs4(req, 'html.parser') #req 문자열을 html관점에서 읽어달라여
    li = dummy.find_all('img') #img있는거 다 찾아라.
    item = str(li[1])
    #seat = (etree.HTML(item)).xpath
    #print(item)
    driver.find_element_by_xpath('//*[@id="TmgsTable"]/tbody/tr/td/img[202]').click() #좌석선택
    time.sleep(1)

    driver.switch_to.default_content()
    # 부모iframe
    while len(driver.find_elements_by_id('ifrmSeat')) == 0:
        pass
    driver.switch_to.frame(driver.find_element_by_id('ifrmSeat'))
    element=driver.find_element_by_xpath('//*[@id="NextStepImage"]')
    driver.execute_script("arguments[0].click();",element)
    #href에 자바스크립트에 함수이름 박음ㄴ 되는거
    #자바스크립트가 잇는 엑스페스를 복사 -> 코드가 존재
    #argument[0](첫번째거) : element 클릭햇을때 거기에 자바스크립트가 있으면 실행해라

def ticket_num():
    element=driver.find_element_by_xpath('//*[@id="PriceRow001"]/td[3]/select')
    driver.execute_script("argument[0].click()",element)

login()
to_page()
select_date()
select_seat()