import pandas
import requests
import json
import os
from datetime import datetime
import re

# EXCEL 저장 정보
column_name_list = [
  '제목',
  '링크',
  '이미지',
  '최저가',
  '최고가',
  '쇼핑몰',
  '상품유형',
  '브랜드',
  '제조사',
  '카테고리1',
  '카테고리2',
  '카테고리3',
  '카테고리4',
  ]


# 오늘 날짜 받아오기
def getDate():
    now = datetime.now()
    nowTime = now.strftime('%Y-%m-%d')
    return nowTime

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
      pass


# NAVER API 호출 함수
def getItemListByNaver (query, display='100', sort='sim'):
  params = {'query': query,'display':display,'sort':sort}
  res = requests.get(URL, headers=headers, params=params)
  resData = json.loads(res.text)['items']
  return resData

# NAVER ITEM 필터링 함수
def getFilteredItemList(itemList):
  def productTypeSpinner(productTypeNumber):
    if productTypeNumber == 1:
      return '일반 - 가격비교 상품'
    if productTypeNumber == 2:
      return '일반 - 가격비교 비매칭 일반상품'
    if productTypeNumber == 3:
      return '일반 - 가격비교 매칭 일반상품'
    if productTypeNumber == 4:
      return '중고 - 가격비교 상품'
    if productTypeNumber == 5:
      return '중고 - 가격비교 비매칭 일반상품'
    if productTypeNumber == 6:
      return '중고- 가격비교 매칭 일반상품'
    if productTypeNumber == 7:
      return '단종 - 가격비교 상품'
    if productTypeNumber == 8:
      return '단종 - 가격비교 비매칭 일반상품'
    if productTypeNumber == 9:
      return '단종 - 가격비교 매칭 일반상품'
    if productTypeNumber == 10:
      return '판매예정 - 가격비교 상품'
    if productTypeNumber == 11:
      return '판매예정 - 가격비교 비매칭 일반상품'
    if productTypeNumber == 12:
      return '판매예정 - 가격비교 매칭 일반상품'
    else:
      return '해당 없음'

  resItemList = []
  itemLen = len(itemList)
  for idx,item in enumerate(itemList):

    item['title'] = re.sub('(<([^>]+)>)', '', item['title'])
    curFilteredItem = {
    'title' : item['title'],
    'link': item['link'],
    'image':item['image'],
    'lprice': item['lprice'],
    'hprice': item['hprice'],
    'mallName': item['mallName'],
    'productType': productTypeSpinner(int(item['productType'])),
    'brand': item['brand'],
    'maker': item['maker'],
    'category1': item['category1'],
    'category2': item['category2'],
    'category3': item['category3'],
    'category4': item['category4'],
    }
    resItemList.append(curFilteredItem.values())

  return resItemList

def saveInExcel(filteredItemList, keyword):
  date = getDate()
  dir_item = './output/item/'+keyword
  dir_date = './output/date/'+date
  file_name = '/'+date+'_'+keyword+'.xlsx'

  createFolder(dir_item)
  createFolder(dir_date)

  df = pandas.DataFrame(filteredItemList, columns=column_name_list)
  df.to_excel("output.xlsx", sheet_name='sample1')
  df.to_excel(dir_item + file_name, sheet_name='sample1')
  df.to_excel(dir_date + file_name, sheet_name='sample1')


# NAVER API 고정 정보
X_NAVER_CLIENT_ID = os.environ.get('X_NAVER_CLIENT_ID')
X_NAVER_CLIENT_SECRET = os.environ.get('X_NAVER_CLIENT_SECRET')
keyword = []

for i in range(0, 10):
  tmp_keyword = os.environ.get('keyword'+str(i))
  keyword.append(tmp_keyword)

URL = 'https://openapi.naver.com/v1/search/shop.json'
headers = {
  'X-Naver-Client-Id': X_NAVER_CLIENT_ID,
  'X-Naver-Client-Secret' : X_NAVER_CLIENT_SECRET
}


for i in range(0, 10):
  query = keyword[i]
  itemList = getItemListByNaver(query)
  filteredItemList = getFilteredItemList(itemList)
  saveInExcel(filteredItemList, query)
