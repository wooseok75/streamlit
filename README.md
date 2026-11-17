# 21_Lab — Streamlit + OpenAI 실습

과제 자료의 실습 3~7 기능을 4개 페이지로 구현한 예시 프로젝트입니다. 실습 8은 GitHub에 push하고 배포 URL을 제출해야 합니다.

## 파일 구성

```text
streamlit_21_lab/
├── streamlit_app.py        # 앱 진입점, API Key 입력, st.navigation
├── helpers.py              # 공통 스트리밍 함수
├── app_pages/
│   ├── Home.py             # 실습 3(텍스트) + 실습 4(이미지)
│   ├── Chat.py             # 실습 5(일반 대화형 챗봇)
│   ├── Chatbot.py          # 실습 6(국립부경대학교 도서관 규정)
│   └── ChatPDF.py          # 실습 7(PDF 검색 챗봇)
├── library_rules.txt       # 규정 일부 요약: 제출 전에 공식 전문으로 교체
├── requirements.txt       # openai (과제 요구대로 한 줄)
└── .gitignore
```

## 1. GitHub Codespaces에서 실행

1. GitHub에서 **공개(Public)** 저장소를 만들고 `Add README`를 선택합니다.
2. 저장소에서 `Code > Codespaces > Create codespace on main`으로 실행합니다.
3. 프로젝트 파일을 저장소에 올립니다. `streamlit_app.py`가 저장소 최상위에 있어야 합니다.
4. Codespaces 터미널에서 다음을 실행합니다.

```bash
pip install streamlit openai
streamlit run streamlit_app.py
```

포트가 열리면 Codespaces에서 `Open in Browser`를 선택합니다. 왼쪽 사이드바에 **OpenAI API Key**를 입력하고 기능을 테스트합니다. API Key를 코드, README, commit, 또는 공개 설정 파일에 저장하지 마세요.

## 2. Chatbot 규정 전문 준비 — 중요

현재 `library_rules.txt`는 **실습 동작을 확인하기 위한 일부 조문 요약**만 포함합니다. 과제의 요구사항은 **규정 전문을 문자열로 넣는 것**이므로, 제출 전에 아래 공식 사이트의 `국립부경대학교 도서관 규정` 전문을 복사하여 이 파일의 내용을 교체하세요.

- 규정 보기: <https://libweb.pknu.ac.kr/guide/intro/regulation/>
- 규정관리시스템: <https://www.pknu.ac.kr/rule/searchSchRegAndRule.do?keywordArr=&pageIndex=6&query1=&query2=&search=1>

교체 후 `Chatbot.py`가 `library_rules.txt`를 읽고 Responses API의 `instructions`에 넣습니다.

테스트 질문:

- 도서관 휴관일은 언제인가요?
- 학부생은 책을 몇 권까지 빌릴 수 있나요?

## 3. ChatPDF 테스트

1. ChatPDF 페이지에서 PDF 파일 하나를 선택합니다.
2. `PDF 분석 시작`을 누르면 OpenAI Files API에 업로드하고 Vector Store를 생성합니다.
3. 인덱싱이 완료되면 문서 내용을 질문합니다.
4. `Clear`: 대화 기록만 지우고 PDF 인덱스는 유지합니다.
5. `Leave`: 원격 Vector Store 및 원본 파일을 삭제하고 업로드 화면으로 돌아갑니다.

과제 추천 테스트 PDF: <https://arxiv.org/pdf/1706.03762>

> Vector Store 생성 및 모델 호출에는 API 비용이 발생할 수 있습니다. 이 앱은 업로드가 성공하면 Streamlit Session State로 해당 인덱스를 재사용하며, Vector Store는 마지막 사용 시점부터 1일 후 만료되도록 설정합니다. 탭을 닫거나 서버가 재시작되면 앱에서 이전 세션에 접근할 수 없으니, 가능하면 `Leave`로 정리한 다음 종료하세요.

## 4. Streamlit Community Cloud에 배포

1. 소스코드를 GitHub 저장소에 `push`합니다.
2. <https://share.streamlit.io/>에 접속합니다.
3. `Create app` → 본인 저장소와 브랜치 선택 → Main file path에 `streamlit_app.py` 입력합니다.
4. API Key를 앱에서 직접 입력하므로 Secrets에는 넣지 않습니다.
5. 배포된 주소에서 Home / Chat / Chatbot / ChatPDF를 테스트합니다.
6. **배포된 웹 앱 링크를 과제 제출란에 제출합니다.**

## 5. 요구사항 확인표

- [x] `st.session_state`에 OpenAI client 저장
- [x] Home 텍스트 질문 + `@st.cache_data`
- [x] Home 이미지 생성 + Base64 디코딩 + spinner
- [x] `st.navigation`, `app_pages` 구성
- [x] Chat 대화 기억, Clear, 스트리밍
- [x] Chatbot 규정 파일을 `instructions`로 전달 (단, 규정 전문은 직접 보완 필요)
- [x] ChatPDF 파일 1개 업로드, File Search, Vector Store 재사용, Clear, Leave
- [ ] GitHub 저장소에 push
- [ ] Streamlit Community Cloud 배포 및 제출

## 참고

- OpenAI Responses API: <https://developers.openai.com/api/docs/guides/streaming-responses>
- OpenAI File Search: <https://developers.openai.com/api/docs/guides/tools-file-search>
- Streamlit Navigation: <https://docs.streamlit.io/develop/api-reference/navigation/st.navigation>

본 예제는 API Key 없이 외부 OpenAI 모델 호출까지 검증할 수는 없습니다. 사용 중인 계정의 사용 권한과 과금 상태에 따라 API 요청이 실패할 수 있습니다.
