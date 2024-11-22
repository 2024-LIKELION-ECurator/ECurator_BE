import requests
from .models import *
from decouple import config

TMDB_API_KEY = config('TMDB_API_KEY')

# 감정에 따른 키워드 정의
EMOTION_KEYWORDS = {
    "happy": ["joyful", "funny", "cheerful", "행복"],
    "sad": ["emotional", "melancholic", "heartfelt", "슬픈"],
    "surprised": ["unexpected", "shocking", "thrilling", "놀라운"],
    "loving": ["romantic", "heartwarming", "sweet", "사랑스러운", "로맨스"],
    "sleepy": ["calming", "soothing", "relaxing", "포근한", "졸린"],
    "nervous": ["thriller", "suspenseful", "tense", "긴장되는", "스릴있는"],
    "pensive": ["thought-provoking", "reflective", "introspective"],
    "relieved": ["uplifting", "light-hearted", "feel-good", "안정", "좋은"],
    "joyful": ["celebratory", "festive", "happy", "즐거운", "신나는"]
}

"""
영화 API
- 최신작중에서 가져와야 하나 로직 고민해야할 듯 &sort_by=popularity.desc
"""
def fetch_and_store_movies(emotion_name):
    try:
        emotion = Emotion.objects.get(name=emotion_name)
    except Emotion.DoesNotExist:
        print(f"Emotion '{emotion_name}' does not exist.")
        return  # 존재하지 않는 감정은 무시

    keywords = EMOTION_KEYWORDS.get(emotion_name, [])
    
    # 영화 리스트 초기화
    movies = []
    
    for keyword in keywords:
        # 국내 영화와 해외 영화를 각각 20개 가져오기
        for region in ['KR', 'US']:  # KR: 한국, US: 미국
            region_movies = []
            page = 1  # page 변수를 초기화

            while len(region_movies) < 20:
                url = f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={keyword}&region={region}&language=ko&include_adult=false&page={page}'
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                except requests.exceptions.Timeout:
                    print(f"Timeout occurred for keyword: {keyword}")
                    break  # 타임아웃 발생 시 루프 탈출
                except requests.exceptions.RequestException as e:
                    print(f"Request failed: {e}")
                    break  # 요청 실패 시 루프 탈출

                data = response.json()
                results = data.get('results', [])
                    
                # 영화 목록에 추가
                for movie in results:
                    if len(region_movies) < 20:  # 20개 미만일 때만 추가
                        region_movies.append(movie)
                    else:
                        break
                    
                page += 1  # 다음 페이지로 이동

                # 결과가 없으면 루프 종료
                if not results:
                    break
                
            # 국내/해외 영화 리스트에 추가
            movies.extend(region_movies)

    # 중복 제거
    unique_movies = {movie['id']: movie for movie in movies}.values()

    # 최대 40개 영화 저장
    count = 0
    for item in unique_movies:
        if count >= 40:
            break
        
        title = item['title']

        # 제목에 "섹스"나 "sex"가 포함되어 있는지 확인
        if "섹스" in title.lower() or "sex" in title.lower():
            continue  # 포함되어 있다면 저장하지 않고 넘어감
        
        # 이미 데이터베이스에 존재하는지 확인
        if Movie.objects.filter(title=title).exists():
            continue  # 제목이 이미 존재하면 저장하지 않고 넘어감

        genre_ids = item['genre_ids']  # 장르 ID 목록
        genre_names = get_genre_names(genre_ids)  # 장르 이름 가져오기
        
        # 감독 정보 가져오기
        author = get_movie_director(item['id'])
        
        # 영화 객체 생성 및 저장
        Movie.objects.create(  # get_or_create 대신 create 사용
            title=title,
            genre=", ".join(genre_names),  # 장르를 쉼표로 구분하여 저장
            author=author,  # 감독 이름 저장
            emotion=emotion  # Emotion 인스턴스를 사용하여 저장
        )
        count += 1


def get_movie_director(movie_id):
    # 특정 영화의 감독 정보를 가져오는 함수
    url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=ko'
    response = requests.get(url)
    data = response.json()
    
    # 감독 이름 추출
    directors = [member['name'] for member in data['crew'] if member['job'] == 'Director']
    return directors[0] if directors else "Unknown"

def get_genre_names(genre_ids):
    # TMDb API에서 장르 ID에 대한 이름을 가져오는 함수
    genre_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US'
    response = requests.get(genre_url)
    genres = response.json().get('genres', [])
    
    genre_dict = {genre['id']: genre['name'] for genre in genres}
    return [genre_dict.get(genre_id, "Unknown") for genre_id in genre_ids]