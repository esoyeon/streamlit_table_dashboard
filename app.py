"""
Streamlit 테이블 대시보드 예제 - 심화편

이 예제는 Streamlit의 다양한 기능을 활용하여 데이터 테이블을 관리하는 방법을 보여줍니다.
기본적인 테이블 편집 기능에 필터링, 컬럼 관리 등 심화 기능을 추가했습니다.

주요 학습 포인트:
1. st.data_editor로 테이블 편집 구현
2. st.sidebar로 필터 및 설정 메뉴 구성
3. st.session_state로 상태 관리
4. st.cache_data로 데이터 캐싱
5. st.columns로 레이아웃 구성
"""

import streamlit as st
import pandas as pd
from config import DATA_PATH

# 페이지 기본 설정
# 대시보드의 기본 레이아웃을 설정합니다
# layout="wide": 화면을 넓게 사용
# initial_sidebar_state="expanded": 사이드바를 펼친 상태로 시작
st.set_page_config(
    page_title="연구 프로젝트 관리 시스템",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# 데이터 로드 함수
@st.cache_data  # 성능 최적화: 동일한 입력에 대해 결과를 재사용합니다
def load_data():
    """
    CSV 파일에서 데이터를 로드하고 전처리합니다.
    
    구현 내용:
    1. CSV 파일 읽기 (pd.read_csv 사용)
    2. 날짜 데이터 변환 (pd.to_datetime 사용)
    3. 빈 값 처리 (fillna 메서드 사용)
    4. 오류 처리 (try-except 구문)
    """
    try:
        df = pd.read_csv(DATA_PATH)
        # 날짜 형식 컬럼 변환
        for col in ["Start_Date", "End_Date"]:
            df[col] = pd.to_datetime(df[col])

        # 빈 값 처리
        df[["Review_Comments", "Action_Items"]] = df[
            ["Review_Comments", "Action_Items"]
        ].fillna("")
        return df
    except Exception as e:
        st.error(f"데이터 파일을 찾을 수 없습니다: {str(e)}")
        return None


# 데이터 저장 함수
def save_data(df):
    """
    수정된 데이터프레임을 CSV 파일로 저장합니다.
    
    구현 내용:
    1. 데이터프레임 복사 (원본 보존)
    2. 날짜 데이터를 문자열로 변환
    3. CSV 파일로 저장
    4. 캐시 초기화 및 사용자 피드백
    """
    try:
        df_to_save = df.copy()
        # 날짜 컬럼을 문자열로 변환
        for col in ["Start_Date", "End_Date"]:
            df_to_save[col] = df_to_save[col].dt.strftime("%Y-%m-%d")

        df_to_save.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
        st.success("데이터가 성공적으로 저장되었습니다!")
        st.cache_data.clear()  # 캐시 초기화로 새로운 데이터 반영
    except Exception as e:
        st.error(f"저장 중 오류가 발생했습니다: {str(e)}")


# 메인 애플리케이션
def main():
    st.title("🔬 연구 프로젝트 관리 시스템")

    # 세션 상태 초기화
    # session_state로 페이지 새로고침 간에 데이터를 유지합니다
    if "data" not in st.session_state:
        st.session_state.data = load_data()

    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False

    if st.session_state.data is None:
        return

    # 사이드바 필터 구현
    # selectbox로 단일 선택 필터를 구현합니다
    st.sidebar.header("필터")

    # 부서 필터: 고유한 부서 목록을 가져와 선택 옵션으로 제공
    departments = ["전체"] + sorted(
        st.session_state.data["Department"].unique().tolist()
    )
    selected_dept = st.sidebar.selectbox("부서", departments)

    # 상태 필터: 고유한 상태 목록을 가져와 선택 옵션으로 제공
    statuses = ["전체"] + sorted(st.session_state.data["Status"].unique().tolist())
    selected_status = st.sidebar.selectbox("상태", statuses)

    # 동적 컬럼 관리 구현
    # multiselect로 다중 선택 기능을 구현합니다
    st.sidebar.header("컬럼 설정")
    hide_columns = st.sidebar.multiselect(
        "숨길 컬럼 선택",
        options=st.session_state.data.columns.tolist(),
        default=[],
        format_func=lambda x: {  # 컬럼명을 한글로 표시
            "Project_ID": "프로젝트 ID",
            "Project_Name": "프로젝트명",
            "Principal_Investigator": "책임자",
            "Department": "부서",
            "Start_Date": "시작일",
            "End_Date": "종료일",
            "Budget": "예산",
            "Progress": "진행률",
            "Research_Area": "연구분야",
            "Status": "상태",
            "Current_Phase": "현재단계",
            "Review_Comments": "검토 의견",
            "Action_Items": "조치 사항",
        }.get(x, x),
    )

    # 필터링 및 컬럼 선택 적용
    display_columns = [
        col for col in st.session_state.data.columns.tolist() if col not in hide_columns
    ]
    filtered_df = st.session_state.data.copy()
    if selected_dept != "전체":
        filtered_df = filtered_df[filtered_df["Department"] == selected_dept]
    if selected_status != "전체":
        filtered_df = filtered_df[filtered_df["Status"] == selected_status]
    filtered_df = filtered_df[display_columns]

    # 레이아웃 구성
    # st.columns를 사용하여 화면 분할
    col1, col2, col3 = st.columns([6, 2, 2])
    with col1:
        if st.toggle("편집 모드", key="edit_toggle"):
            st.session_state.edit_mode = True
        else:
            st.session_state.edit_mode = False

        edit_mode = st.session_state.edit_mode

    # 데이터 테이블 표시
    # 편집 모드에 따라 다른 형태의 테이블 표시
    if edit_mode:
        st.warning("⚠️ 변경사항을 저장하지 않으면 수정한 내용이 사라집니다.")
        edited_df = st.data_editor(
            filtered_df,
            column_config={
                "Project_ID": st.column_config.TextColumn(
                    "프로젝트 ID",
                    width="small",
                    disabled=True,
                ),
                "Project_Name": st.column_config.TextColumn(
                    "프로젝트명",
                    width="medium",
                    disabled=True,
                ),
                "Principal_Investigator": st.column_config.TextColumn(
                    "책자",
                    width="small",
                ),
                "Department": st.column_config.TextColumn(
                    "부서",
                    width="small",
                ),
                "Start_Date": st.column_config.DateColumn(
                    "시작일",
                    width="small",
                    format="YYYY-MM-DD",
                ),
                "End_Date": st.column_config.DateColumn(
                    "종료일",
                    width="small",
                    format="YYYY-MM-DD",
                ),
                "Budget": st.column_config.NumberColumn(
                    "예산",
                    width="small",
                    format="%d원",
                ),
                "Progress": st.column_config.ProgressColumn(
                    "진행률",
                    width="small",
                    min_value=0,
                    max_value=100,
                ),
                "Research_Area": st.column_config.TextColumn(
                    "연구분야",
                    width="small",
                ),
                "Status": st.column_config.SelectboxColumn(
                    "상태",
                    width="small",
                    options=["진행중", "완료", "중단", "검토중", "준비중"],
                ),
                "Current_Phase": st.column_config.SelectboxColumn(
                    "현재단계",
                    width="small",
                    options=[
                        "계획",
                        "실험",
                        "데이터수집",
                        "분석",
                        "검증",
                        "논문작성",
                        "특허출원",
                    ],
                ),
                "Review_Comments": st.column_config.TextColumn(
                    "검토 의견",
                    width="medium",
                    help="프로젝트에 대한 검토 의견을 입력하세요",
                ),
                "Action_Items": st.column_config.TextColumn(
                    "조치 사항",
                    width="medium",
                    help="필요한 조치 사항을 입력하세요",
                ),
            },
            use_container_width=True,
            num_rows="dynamic",
            height=500,
            key="editor",
            hide_index=False,
        )

        # 저장 버튼 구현
        with col3:
            if st.button("변경사항 저장", type="primary", use_container_width=True):
                for idx in filtered_df.index:
                    st.session_state.data.loc[idx] = edited_df.loc[idx]
                save_data(st.session_state.data)
                st.session_state.edit_mode = False
                st.rerun()
    else:
        # 읽기 전용 모드 테이블
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=False,
            height=500,
        )

    # 필터링 결과 요약 표시
    st.sidebar.markdown("---")
    st.sidebar.info("📊 현재 표시된 프로젝트 통계")
    st.sidebar.markdown(f"- 전체 프로젝트: {len(st.session_state.data)}개")
    st.sidebar.markdown(f"- 필터링된 프로젝트: {len(filtered_df)}개")


if __name__ == "__main__":
    main()
