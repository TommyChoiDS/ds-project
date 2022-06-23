# 중고차 가격 예측 웹서비스 구축 프로젝트

21.10.06 - 21.10.13

차량 정보 기반 중고차 가격 예측 웹서비스 구축 프로젝트

사용 기술 : Pandas, BeautifulSoup, Selenium, CatBoost, Flask, PostgreSQL

---

- 사용자로부터 차량 정보를 입력받아 중고차 가격을 예측하는 웹서비스
- 중고차 매매 사이트에서 차량 매물 데이터를 크롤링하여 모델링한 후 Flask앱으로 배포하여 사용자들이 예상 중고차 가격을 알아볼 수 있도록 함
- 동적 웹페이지 크롤링을 위해 Selenium과 BeautifulSoup4를 이용
- 크롤링한 데이터는 PostgreSQL에 저장하고 CatBoost로 모델링
    - CatBoost R-Squared Score : 0.90
- Pickle을 통해 머신러닝 모델 Flask 프레임워크에 서빙
    - Flask를 통한 애플리케이션 제작 및 Heroku를 통한 배포
