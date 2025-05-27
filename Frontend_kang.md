# 📚 도서 검색 웹 애플리케이션

사용자가 도서를 검색하고 상세 정보를 확인할 수 있는 웹 프론트엔드 애플리케이션입니다.

## 🔍 주요 기능

- 키워드를 기반으로 도서 검색
- 도서 목록 조회 및 정렬
- 도서 상세 정보 확인
- 사용자 친화적인 UI 및 반응형 디자인

## 🛠️ 기술 스택

- **Frontend Framework**: Vue.js / React.js (택 1)
- **UI Framework**: Tailwind CSS 
- **HTTP 통신**: Axios
- **상태 관리**: Pinia / Vuex / React Query 등 (해당 시)
- **계정 API**: Kakao API / Google Books API 등
- **도서 API**: Kakao Book API / Google Books API 등


## 📂 프로젝트 구조

src/
├── components/ # 재사용 가능한 컴포넌트
├── views/ # 페이지 단위 컴포넌트
├── router/ # 라우팅 설정
├── store/ # 상태 관리
├── assets/ # 이미지 및 스타일
├── App.vue # 루트 컴포넌트
└── main.js # 앱 진입점


## 🖥️ 페이지 구성

- **홈 (HomeView)**: 검색창 및 검색 결과 미리 보기
- **도서 목록 (BookListView)**: 키워드 기반 검색 결과 출력
- **도서 상세 (BookDetailView)**: 도서 이미지, 설명, 출판 정보 등 표시

## 🚀 시작하기

```bash
# 프로젝트 클론
git clone https://github.com/your-username/book-search-app.git
cd book-search-app

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
