import requests  # 웹 페이지 요청을 보낼 때 사용
from bs4 import BeautifulSoup  # HTML을 파싱(분석)할 때 사용

def get_latest_news_url():
    # 뉴욕타임스 모닝 브리핑 페이지 URL
    url = "https://www.nytimes.com/newsletters/morning-briefing"
    
    # 해당 URL로 HTTP GET 요청을 보냄
    response = requests.get(url)

    # 만약 요청이 실패하면(응답 코드가 200이 아니면) 오류 메시지를 출력하고 None 반환
    if response.status_code != 200:
        print("❌ 뉴스 페이지 크롤링 실패")  # 실패 메시지 출력
        return None

    # HTML을 BeautifulSoup을 이용해 파싱
    soup = BeautifulSoup(response.text, "html.parser")

    # "Read the Latest"라는 텍스트를 가진 <a> 태그(버튼)를 찾음
    button = soup.find("a", string="Read the Latest")

    # 버튼이 존재하는 경우
    if button:
        latest_news_url = button["href"]  # <a> 태그의 href 속성(링크) 가져오기

        # 만약 링크가 상대 경로로 되어 있으면 절대 경로로 변환
        if latest_news_url.startswith("/"):
            latest_news_url = "https://www.nytimes.com" + latest_news_url  

        return latest_news_url  # 최신 뉴스 링크 반환

    else:
        # "Read the Latest" 버튼을 찾지 못한 경우 오류 메시지 출력
        print("❌ 'Read the Latest' 버튼을 찾을 수 없음")
        return None

# 실행 테스트: 함수 호출 후 반환된 최신 뉴스 URL 출력
latest_news_url = get_latest_news_url()
print("Latest News URL:", latest_news_url)



