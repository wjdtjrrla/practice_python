import pandas as pd
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver

# 브라우져 오픈
driver = webdriver.Chrome()

# base_url 생성
base_url = 'https://finance.naver.com'
# sub_url 생성
sub_url = '/item/main.naver?code='
# 종목 코드 
# code = input("종목 코드를 입력해주세요. : ")
code = '000660'
# 특정 웹페이지 이동
driver.get(base_url + sub_url + code)
time.sleep(2)
# 해당 페이지 html 소스 코드 파싱
soup = bs(driver.page_source,'html.parser')


# div 코드 중 class가 news_section 태그 선택
div_data = soup.find(
    'div',
    attrs = {
        'class' : 'news_section'
    }
)

# div 코드 중 li 태그 모두 찾기
li_list = div_data.find_all('li')

# li 태그 중 첫번째 a태그 href 속성 값 리스트 생성
href_list = list(
    map(
        # lambda li_data : li_data.find('a')['href']
        lambda li_data : li_data.a['href'],
        li_list
    )
)

#뉴스의 기사들을 저장할 수 있는 리스트 생성
result = []
#href_list를 이용해서 반복문 실행
for href in href_list:
    try:
        driver.get(base_url+href)
        news_soup = bs(driver.page_source,'html.parser')
        
        news_title = news_soup.find('h2',attrs={'id':'title_area'}).get_text()
        news_content = news_soup.find('div',attrs={'id':'newsct_article'}).get_text().replace('\n','').replace('\t','')
        
        news_dict = {
            'title' : news_title,
            'content' : news_content
        }
        result.append(news_dict)
    except:
        continue
# 결과를 데이터프레임으로 변환
df = pd.DataFrame(result)
print(df)


# 데이터프레임 csv파일로 저장
df.to_csv(f'news_{code}.csv',index=False)