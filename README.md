# Streamlit 테이블 대시보드 예제

이 프로젝트는 Streamlit의 데이터 처리 및 대시보드 기능을 보여주는 심화 예제입니다.
기본적인 테이블 편집 기능에 필터링, 컬럼 관리 등 추가 기능을 구현했습니다.

## 학습 목표

이 예제를 통해 다음 Streamlit 기능들을 배울 수 있습니다:
- `st.data_editor`를 사용한 테이블 데이터 편집
- `st.sidebar`를 활용한 필터 구현
- `st.columns`을 이용한 레이아웃 구성
- `st.multiselect`로 동적 컬럼 관리
- `st.cache_data`를 통한 데이터 캐싱
- 세션 상태(session state) 관리

## 데모
실제 동작하는 예제는 다음 [링크](https://pandas-edit-dashboard.streamlit.app/)에서 확인할 수 있습니다

## 주요 기능 구현

1. **데이터 편집**
   - 테이블 실시간 수정
   - 변경사항 저장/복구

2. **필터링**
   - 사이드바를 이용한 카테고리 필터
   - 다중 조건 필터링

3. **컬럼 관리**
   - 동적 컬럼 표시/숨김
   - 컬럼 설정 저장

4. **상태 관리**
   - 세션 상태를 통한 데이터 관리
   - 캐시를 이용한 성능 최적화

## 실행 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 애플리케이션 실행:
```bash
streamlit run app.py
```

## 프로젝트 구조
```
streamlit_table_dashboard/
├── app.py          # 메인 애플리케이션
├── config.py       # 설정 파일
├── requirements.txt # 필요한 패키지 목록
└── data/           # 데이터 저장 폴더
```

## 참고 자료
- [Streamlit 공식 문서](https://docs.streamlit.io/)
- [st.data_editor API 참조](https://docs.streamlit.io/library/api-reference/data/st.data_editor)
- [세션 상태 가이드](https://docs.streamlit.io/library/api-reference/session-state)