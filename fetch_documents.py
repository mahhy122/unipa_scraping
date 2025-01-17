import requests
import datetime
from bs4 import BeautifulSoup
import warnings;from bs4.builder import XMLParsedAsHTMLWarning;warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

from dotenv import load_dotenv
import os

load_dotenv()
UNIPA_ID = os.getenv('UNIPA_ID')
UNIPA_PASSWORD = os.getenv('UNIPA_PASSWORD')
DIRECTORY = os.getenv('DIRECTORY')

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
weekday = now.weekday()
today_date = now.date().strftime('%Y/%m/%d')

def ent(ent_soup):
  w = ent_soup.find('input', attrs={'name': 'rx-token'})
  token = w.get('value')
  x = ent_soup.find("input",attrs = {'name':'rx-loginKey'})
  loginkey = x.get("value")
  y = ent_soup.find("input",attrs = {'name':'javax.faces.ViewState'})
  javax = y.get("value")
  z = ent_soup.find("form",attrs={"method":"post"})
  link = z.get("action")
  return token,loginkey,javax,link

login_url = "https://unipa.u-hyogo.ac.jp/uprx/"
session = requests.session()
session.get(login_url)

def g_script(url,data):
  respons = session.post(url, data=data)
  soup = BeautifulSoup(respons.text, 'lxml')
  return soup

def enter_unipa():
  #ログイン
  login_payload = {"loginForm": "loginForm",
    "loginForm:userId" : UNIPA_ID,
    "loginForm:password": UNIPA_PASSWORD,
    "loginForm:loginButton":"",
    "javax.faces.ViewState": "stateless"
  }
  login_soup = g_script(login_url,login_payload)

  #トップ画面
  token,loginkey,javax,link = ent(login_soup)
  ent1_url = "https://unipa.u-hyogo.ac.jp"+str(link)
  data1 ={
    "headerForm": "headerForm"
    ,"rx-token": token
    ,"rx-loginKey": loginkey
    ,"rx-deviceKbn": "1"
    ,"headerForm:logo": ""
    ,"javax.faces.ViewState": javax
    ,"rx.sync.source": "headerForm:logo"
  }
  ent1_soup = g_script(ent1_url,data1)

  #クラスプロファイル
  token,loginkey,javax,link = ent(ent1_soup)
  ent2_url = "https://unipa.u-hyogo.ac.jp"+str(link)
  data2 = {
    "funcForm": "funcForm",
    "rx-token": token,
    "rx-loginKey": loginkey,
    "rx-deviceKbn": "1",
    "funcForm:j_idt162_activeIndex": "0",
    "funcForm:j_idt361:j_idt1767:j_idt1767_input": today_date,
    "funcForm:j_idt361:j_idt1808:0:jugyoMemo": "",
    "funcForm:j_idt361:j_idt1808:1:jugyoMemo": "",
    "funcForm:j_idt361:j_idt1808:2:jugyoMemo": "",
    "funcForm:j_idt361:j_idt1808:3:jugyoMemo": "",
    "funcForm:j_idt361:content_view": "month",
    "funcForm:j_idt361:j_idt2402:0:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:1:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:2:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:3:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:4:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:5:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:6:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:7:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:8:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:9:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:10:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:11:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:12:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:13:jugyoMemo": "",
    "funcForm:j_idt361:j_idt2402:14:jugyoMemo": "",
    "funcForm:j_idt361_activeIndex": "0",
    "javax.faces.ViewState": javax,
    "rx.sync.source": "funcForm:j_idt361:j_idt518:j_idt524",
    "funcForm:j_idt361:j_idt518:j_idt524": "funcForm:j_idt361:j_idt518:j_idt524"
  }
  ent2_soup = g_script(ent2_url,data2)
  print(ent2_soup.find_all("span",class_="span"))

  #授業資料
  token,loginkey,javax,link = ent(ent2_soup)
  ent3_url = "https://unipa.u-hyogo.ac.jp"+str(link)
  data3 = {
    "functionHeaderForm": "functionHeaderForm"
    ,"rx-token": token
    ,"rx-loginKey": loginkey
    ,"rx-deviceKbn": "1"
    ,"functionHeaderForm:j_idt159:3:j_idt162": ""
    ,"javax.faces.ViewState": javax
    ,"rx.sync.source": "functionHeaderForm:j_idt159:3:j_idt162"
  }

  
  ent3_soup = g_script(ent3_url,data3)
  print(ent3_soup.find_all("div",class_ = "cpTgtName")[0].text)
  return ent3_soup

def search_unread(lecture_date, lecture_order, ent3_soup):
  #授業選択
  lecture_contents1 = [["192","195","200"],["206","209","214"],["220","223","228"],["234","237","242"],["248","251","256"],["290","294"]]
  token,loginkey,javax,link = ent(ent3_soup)
  ent4_url = "https://unipa.u-hyogo.ac.jp"+str(link)
  data4 = {
    "funcLeftForm": "funcLeftForm"
    ,"rx-token": token
    ,"rx-loginKey": loginkey
    ,"rx-deviceKbn": "1"
    ,"funcLeftForm:j_idt"+lecture_contents1[lecture_date][0]+":"+str(lecture_order)+":j_idt"+lecture_contents1[lecture_date][1]+":0:j_idt"+lecture_contents1[lecture_date][2]: ""
    ,"javax.faces.ViewState": javax
    ,"rx.sync.source": "funcLeftForm:j_idt"+lecture_contents1[lecture_date][0]+":"+str(lecture_order)+":j_idt"+lecture_contents1[lecture_date][1]+":0:j_idt"+lecture_contents1[lecture_date][2]
  }
  ent4_soup = g_script(ent4_url,data4)

  
  unread_list = []
  for count, elem in enumerate(ent4_soup.find_all("td",class_="colSize4 alignCenter"),start=0):
    #unread_list.append(elem.text)
    
    if elem.text != "":
      if len(elem.parent.find_all("a")) > 0:
        unread_list.append(count)
      else:
        unread_list.append(-1)
  return unread_list, ent4_soup

def get_file(lecture_date,lecture_order,ent_soup,message_order):    
  #資料オープン
  token,loginkey,javax,link = ent(ent_soup)

  w = ent_soup.find('input', attrs={'name': 'rx-token'})
  token = w.get('value') # type: ignore
  x = ent_soup.find("input",attrs = {'name':'rx-loginKey'})
  loginkey = x.get("value")# type: ignore

  ent5_url = "https://unipa.u-hyogo.ac.jp"+str(link)
  data5 = {
    "javax.faces.partial.ajax": "true"
    ,"javax.faces.source": "funcForm:jgdocList:"+str(message_order)+":j_idt339"
    ,"javax.faces.partial.execute": "funcForm:jgdocList:"+str(message_order)+":j_idt339"
    ,"funcForm:jgdocList:"+str(message_order)+":j_idt339": "funcForm:jgdocList:"+str(message_order)+":j_idt339"
    ,"funcForm": "funcForm"
    ,"rx-token": token
    ,"rx-loginKey": loginkey
    ,"rx-deviceKbn": "1"
    ,"funcForm:jgdocGrpNo_focus": ""
    ,"funcForm:jgdocGrpNo_input": ""
    ,"funcForm:jgdocName": ""
    ,"javax.faces.ViewState": javax
  }
  ent5_soup = g_script(ent5_url, data=data5)

  #課題情報取得
  file_nunber = 0
  for elem in ent5_soup.find_all("span",class_="ui-button-text ui-c"):
    if elem.text == '添付資料を確認':
      file_nunber =[]
      w = ent5_soup.find('input', attrs={'name': 'rx-token'})
      token = w.get('value') # type: ignore
      x = ent5_soup.find("input",attrs = {'name':'rx-loginKey'})
      loginkey = x.get("value")# type: ignore

      ent6_url = "https://unipa.u-hyogo.ac.jp"+"/uprx/up/jg/jga023/Jga02302.xhtml"
      data6 = {
        "javax.faces.partial.ajax": "true",
        "javax.faces.source": "funcForm:j_idt368",
        "javax.faces.partial.execute": "funcForm:j_idt366",
        "funcForm:j_idt368": "funcForm:j_idt368",
        "funcForm": "funcForm",
        "rx-token": token,
        "rx-loginKey": loginkey,
        "rx-deviceKbn": "1",
        "javax.faces.ViewState": javax
      }
      ent6_soup = g_script(ent6_url, data=data6)
      for elem in ent6_soup.find_all("div",class_="fileListCell downLoadCellFilNm"):
        file_nunber.append(elem.text)
      file_nunber =len(file_nunber)

      lecture_contents2 = [["203","206","211"],["217","220","225"],["231","234","239"],["245","248","253"],["259","262","267"],["301","305"]]

      w = ent6_soup.find('input', attrs={'name': 'rx-token'})
      token = w.get('value')# type: ignore
      x = ent6_soup.find("input",attrs = {'name':'rx-loginKey'})
      loginkey = x.get("value")# type: ignore
      z = ent6_soup.find("form",attrs={"method":"post"})
      link = z.get("action")# type: ignore

      ent7_url = "https://unipa.u-hyogo.ac.jp"+str(link)
      data7 = {
        "funcLeftForm": "funcLeftForm"
        ,"rx-token": token
        ,"rx-loginKey": loginkey
        ,"rx-deviceKbn": "1"
        ,"funcLeftForm:j_idt"+lecture_contents2[lecture_date][0]+":"+str(lecture_order)+":j_idt"+lecture_contents2[lecture_date][1]+":0:j_idt"+lecture_contents2[lecture_date][2]: ""
        ,"javax.faces.ViewState": javax
        ,"rx.sync.source": "funcLeftForm:j_idt"+lecture_contents2[lecture_date][0]+":"+str(lecture_order)+":j_idt"+lecture_contents2[lecture_date][1]+":0:j_idt"+lecture_contents2[lecture_date][2]
      }
      ent5_soup = g_script(ent7_url,data7)
  
      
  return file_nunber, ent5_soup

def document_downloader(lecture_date,lecture_order,weekday,message_order,file_number):
  chrome_options = webdriver.ChromeOptions()
  prefs = {
    "download.default_directory": DIRECTORY  # ダウンロードフォルダ
  }
  chrome_options.add_experimental_option("prefs", prefs)

  # ChromeDriverのパスを設定してWebDriverを初期化
  driver = webdriver.Chrome(
    executable_path="D:\\code_project\\python_project\\unipa\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe",
    options=chrome_options
  )

  driver.get("https://unipa.u-hyogo.ac.jp/uprx/up/jg/jga001/Jga00101.xhtml")
  id_list = [UNIPA_ID, UNIPA_PASSWORD]

  #ログイン
  driver.find_element(By.ID, "loginForm:userId").send_keys(id_list[0])
  driver.find_element(By.ID, "loginForm:password").send_keys(id_list[1])
  driver.find_element(By.ID, "loginForm:loginButton").click()
  sleep(2)

  #クラスプロファイル
  driver.find_element(By.ID, "funcForm:j_idt361:j_idt518:j_idt524").click()
  sleep(1)

  if file_number > 0:
    tab_number = lecture_date+1
    lecture_contents = [["202","205","208"],["216","219","222"],["230","233","236"],["244","247","250"],["258","261","264"],["300","302"]]
    if weekday >4:
      weekday = 0
    if weekday != tab_number-1:
      #授業のタブを開く
      driver.find_element(By.ID, "funcLeftForm:yobiPanel"+str(tab_number)+"_toggler").click()
      sleep(0.5)
    sleep(0.1)
    #授業選択
    driver.find_element(By.ID, "funcLeftForm:j_idt"+lecture_contents[lecture_date][0]+":"+str(lecture_order)+":j_idt"+lecture_contents[lecture_date][1]+":0:j_idt"+lecture_contents[lecture_date][2]).click()
    sleep(0.5)
    #授業資料タブを選択
    driver.find_element(By.ID, "functionHeaderForm:j_idt159:3:j_idt161").click()
    sleep(0.8)
    #資料の選択
    driver.find_element(By.ID, "funcForm:jgdocList:"+str(message_order)+":j_idt339").click()
    sleep(0.8)
    driver.find_element(By.ID, "funcForm:j_idt368").click()
    sleep(0.8)
    for k in range(file_number):
      driver.find_element(By.ID, "pkx02201:ch:appendList:"+str(k)+":j_idt443").click()
      sleep(8)
    sleep(8)
  return

lecture_list = [[0,1,2,3],[0,1],[0],[0,1,2,3],[0,1,2,3]]
box = []


for lecture_date in range(len(lecture_list)):
  arry1 = []
  for lecture_order in lecture_list[lecture_date]:
    soup = enter_unipa()
    unreadlist, soup = search_unread(lecture_date, lecture_order, soup)
    arry2 = []
    print(unreadlist)
    for unread in unreadlist:
      if unread != -1:

        filenumber, soup = get_file(lecture_date, lecture_list, soup, unread)
        print([unread, filenumber])
        arry2.append([unread, filenumber])
    arry1.append(arry2)
  box.append(arry1)
print(box)
 
for i in range(len(box)):
  for j in range(len(box[i])):
    for k in range(len(box[i][j])):
      document_downloader(i, j, weekday, box[i][j][k][0], box[i][j][k][1])

"""
lecture_date = 1
lecture_list = 0
soup = enter_unipa()
for i in range(2):
  unreadlist, soup2 = search_unread(1,i,soup)
  filenumber, soup = get_file(lecture_date, i, soup, 0)
  print([0, filenumber])
  print(soup)

#document_downloader(0,0,weekday,1,filenumber)"""
