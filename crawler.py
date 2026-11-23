import json
import requests
from bs4 import BeautifulSoup

def fetch_wonju_events():
    url = "https://www.wonju.go.kr/tour/selectBbsNttList.do?bbsNo=85&key=1921"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    events = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        rows = soup.select('.board-table tbody tr')
        
        for idx, row in enumerate(rows[:10]):
            title_elem = row.select_one('.subject a')
            date_elem = row.select_one('.date')
            
            if title_elem:
                title = title_elem.text.strip()
                link = "https://www.wonju.go.kr/tour/" + title_elem.get('href', '')
                reg_date = date_elem.text.strip() if date_elem else "2026-11-23"
                
                events.append({
                    "id": f"wonju_gov_{idx+1}",
                    "title": title,
                    "subtitle": title,
                    "theme": "원주시청 공식 공지 행사",
                    "category": "원주시 소식",
                    "color": "#008080",
                    "startDate": reg_date,
                    "endDate": reg_date,
                    "time": "방문 전 공식 공지 확인 필요",
                    "location": "원주시 일원",
                    "address": "강원특별자치도 원주시",
                    "fee": "방문 전 공식 공지 확인 필요",
                    "organizer": "원주시청",
                    "contact": "033-737-2114",
                    "description": f"원주시청 공식 게시판에 등록된 행사입니다. 상세 정보는 홈페이지({link})를 참고하세요.",
                    "image": "https://via.placeholder.com/600x400/008080/ffffff?text=Wonju+City+Event"
                })
                
    except Exception as e:
        print(f"크롤링 오류 발생: {e}")

    # 크롤링 실패 또는 목록이 빌 경우 기본 예시 데이터 유지
    if not events:
        events = [
            {
                "id": "festival2026",
                "title": "2026 원주 그림책페스티벌",
                "subtitle": "원주 그림책페스티벌",
                "theme": "새로운 독자, 환대의 노래",
                "category": "원주 그림책페스티벌",
                "color": "#008080",
                "startDate": "2026-11-06",
                "endDate": "2026-11-29",
                "time": "10:00 ~ 18:00 (휴관일 없음)",
                "location": "원주남산골문화센터",
                "address": "강원특별자치도 원주시 향교길 77",
                "fee": "무료 · 전체 관람",
                "organizer": "원주시 / 사회적협동조합 그림책도시",
                "contact": "033-734-0755",
                "description": "그림책으로 인간과 동물, 식물 등 낯선 존재들을 새로운 독자로 만나고 공존과 환대의 가치를 나누는 전시",
                "image": "https://via.placeholder.com/600x400/ffe4b5/333333?text=Wonju+PictureBook+Festival"
            }
        ]

    with open('events.json', 'w', encoding='utf-8') as f:
        json.dump(events, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    fetch_wonju_events()
