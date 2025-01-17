import requests
import datetime
from bs4 import BeautifulSoup
import warnings;from bs4.builder import XMLParsedAsHTMLWarning;warnings.filterwarnings('ignore', category=XMLParsedAsHTMLWarning)

from dotenv import load_dotenv
import os

load_dotenv()
UNIPA_ID = os.getenv('UNIPA_ID')
UNIPA_PASSWORD = os.getenv('UNIPA_PASSWORD')

t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')
now = datetime.datetime.now(JST)
today_date = now.date().strftime('%Y/%m/%d')

#授業
#lecture_date = 1
#lecture_order = 0

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

def get_soup():
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
    "funcForm": "funcForm"
    ,"rx-token": token
    ,"rx-loginKey": loginkey
    ,"rx-deviceKbn": "1"
    ,"funcForm:j_idt162_activeIndex": "0"
    ,"funcForm:j_idt361:j_idt1767:j_idt1767_input": today_date
    ,"funcForm:j_idt361:j_idt1808:0:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt1808:1:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt1808:2:jugyoMemo": ""
    ,"funcForm:j_idt361:content_view": "month"
    ,"funcForm:j_idt361:j_idt2402:0:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:1:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:2:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:3:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:4:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:5:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:6:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:7:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:8:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:9:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:10:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:11:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:12:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:13:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:14:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:15:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:16:jugyoMemo": ""
    ,"funcForm:j_idt361:j_idt2402:17:jugyoMemo": ""
    ,"funcForm:j_idt361_activeIndex": "0"
    ,"javax.faces.ViewState": javax
    ,"rx.sync.source": "funcForm:j_idt361:j_idt518:j_idt524"
    ,"funcForm:j_idt361:j_idt518:j_idt524": "funcForm:j_idt361:j_idt518:j_idt524"
  }
  ent2_soup = g_script(ent2_url,data2)

  #課題閲覧
  token,loginkey,javax,link = ent(ent2_soup)
  ent3_url = "https://unipa.u-hyogo.ac.jp"+str(link)
  data3 = {
    "functionHeaderForm": "functionHeaderForm",
    "rx-token": token,
    "rx-loginKey": loginkey,
    "rx-deviceKbn": "1",
    "functionHeaderForm:j_idt159:1:j_idt162": "",
    "javax.faces.ViewState": javax,
    "rx.sync.source": "functionHeaderForm:j_idt159:1:j_idt162"
  }
  ent3_soup = g_script(ent3_url,data3)
  return ent3_soup

def get_lecuture(lecture_date, lecture_order, ent3_soup):
  #授業選択
  lecture_contents = [["192","195","200"],["206","209","214"],["220","223","228"],["234","237","242"],["248","251","256"],["300","304"]]
  token,loginkey,javax,link = ent(ent3_soup)
  ent4_url = "https://unipa.u-hyogo.ac.jp"+str(link)
  data4 = {
    "funcLeftForm": "funcLeftForm",
    "rx-token": token,
    "rx-loginKey": loginkey,
    "rx-deviceKbn": "1",
    "funcLeftForm:j_idt"+lecture_contents[lecture_date][0]+":"+str(lecture_order)+":j_idt"+lecture_contents[lecture_date][1]+":0:j_idt"+lecture_contents[lecture_date][2]: "",
    "funcLeftForm:yobiPanel1_collapsed": "false",
    "funcLeftForm:yobiPanel2_collapsed": "true",
    "funcLeftForm:yobiPanel3_collapsed": "true",
    "funcLeftForm:yobiPanel4_collapsed": "true",
    "funcLeftForm:yobiPanel5_collapsed": "true",
    "javax.faces.ViewState": javax,
    "rx.sync.source": "funcLeftForm:j_idt"+lecture_contents[lecture_date][0]+":"+str(lecture_order)+":j_idt"+lecture_contents[lecture_date][1]+":0:j_idt"+lecture_contents[lecture_date][2]
  }
  ent4_soup = g_script(ent4_url,data4)

  #課題データの編集
  status_list = []
  count = 0
  for i,elem in enumerate(ent4_soup.find_all("span",attrs={'class': ["sign signEndAccept","sign signAccepting","sign signEndSubmit","sign signNowAvailable","sign signStillAccept"]})):
    status_list.append([elem.text.replace(" ","").replace("\n",""),ent4_soup.find_all("a",class_="ui-commandlink ui-widget")[i].text])
  a=[]
  for i, elem in enumerate(ent4_soup.find_all("span",attrs={'class': ["dateDisp"]})):
    a.append(elem.text)
    if (i+1)%4 == 0:
      status_list[count].append(a)
      a=[]
      count += 1
  homework_list = [ent4_soup.find_all("div",class_="cpTgtName")[0].text.replace("ui-button\n","")]
  for j in range(len(status_list)):             
    if status_list[j][0]=="提出受付中":
      homework_list.append(status_list[j])
  
  return homework_list, ent4_soup

homework_list = []
lecture_list = [[0,1,2,3],[0,1],[0],[0,1,2,3],[0,1,2,3]]
ent_soup = get_soup()
for i in range(5):
  for j in lecture_list[i]:
    arry, ent_soup = get_lecuture(i,j,ent_soup)
    if len(arry)>1:
      homework_list.append(arry)
print(homework_list)
