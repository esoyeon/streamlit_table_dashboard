"""
Streamlit 테이블 대시보드 예제 - 심화편

이 예제는 기본적인 테이블 편집 기능에 필터링, 컬럼 관리 등 추가 기능을 구현한 예제입니다.
Streamlit의 다양한 위젯들을 활용하여 실용적인 데이터 관리 대시보드를 만드는 방법을 보여줍니다.

주요 학습 포인트:
1. st.data_editor로 테이블 편집 구현하기
   - 컬럼 설정 (column_config)
   - 데이터 유효성 검사
   - 실시간 데이터 수정

2. st.sidebar로 필터 및 설정 메뉴 구성하기
   - selectbox로 필터 만들기
   - multiselect로 다중 선택 구현

3. st.session_state로 상태 관리하기
   - 페이지 새로고침 간 데이터 유지
   - 편집 모드 상태 관리

4. st.cache_data로 데이터 캐싱하기
   - 성능 최적화
   - 데이터 재사용

5. st.columns로 레이아웃 구성하기
   - 화면 분할
   - 요소 배치
"""

# 페이지 기본 설정
# 반드시 다른 Streamlit 명령어보다 먼저 실행되어야 함
import streamlit as st

st.set_page_config(
    page_title="연구 프로젝트 관리 시스템",
    page_icon="🔬",
    layout="wide",  # 페이지를 wide 모드로 설정
    initial_sidebar_state="expanded",  # 사이드바를 펼친 상태로 시작
)

import pandas as pd
from config import DATA_PATH


# 테이블 컬럼 설정
# 편집 모드와 보기 모드에서 공통으로 사용할 컬럼 설정
def get_column_config(is_edit_mode=False):
    """
    테이블의 컬럼 설정을 반환합니다.

    각 컬럼의 특성에 맞는 적절한 컴포넌트를 설정합니다:
    - TextColumn: 일반 텍스트 입력
    - DateColumn: 날짜 선택기
    - NumberColumn: 숫자 입력 (포맷팅 가능)
    - ProgressColumn: 진행률 표시
    - SelectboxColumn: 드롭다운 선택

    Args:
        is_edit_mode (bool): 편집 모드 여부. True일 경우 일부 컬럼이 선택 가능한 형태로 변경됩니다.

    Returns:
        dict: 컬럼 설정 딕셔너리
    """
    base_config = {
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
            "책임자",
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
    }

    # 편집 모드일 때는 선택 가능한 컬럼으로 변경
    if is_edit_mode:
        base_config.update(
            {
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
            }
        )
    else:
        base_config.update(
            {
                "Status": st.column_config.TextColumn(
                    "상태",
                    width="small",
                ),
                "Current_Phase": st.column_config.TextColumn(
                    "현재단계",
                    width="small",
                ),
            }
        )

    return base_config


@st.cache_data  # 캐시 데코레이터: 동일한 입력에 대해 결과를 재사용하여 성능 향상
def load_data():
    """
    CSV 파일에서 데이터를 로드하고 전처리합니다.

    주요 기능:
    1. CSV 파일 읽기 (pandas 사용)
    2. 날짜 데이터 변환 (datetime 형식으로)
    3. 결측치 처리 (빈 문자열로 대체)
    4. 오류 리 (파일이 없는 경우 등)

    Returns:
        DataFrame: 전처리된 데이터프레임
        None: 오류 발생 시
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


def save_data(df):
    """
    데이터프레임을 CSV 파일로 저장합니다.

    주요 기능:
    1. 데이터프레임 복사 (원본 보존)
    2. 날짜 데이터를 문자열로 변환
    3. CSV 파일로 저장
    4. 캐시 초기화 (새로운 데이터 반영을 위해)
    5. 성공/실패 메시지 표시

    Args:
        df (DataFrame): 저장할 데이터프레임
    """
    try:
        df_to_save = df.copy()
        for col in ["Start_Date", "End_Date"]:
            df_to_save[col] = df_to_save[col].dt.strftime("%Y-%m-%d")
        df_to_save.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
        st.success("데이터가 성공적으로 저장되었습니다!")
        st.cache_data.clear()
    except Exception as e:
        st.error(f"저장 중 오류가 발생했습니다: {str(e)}")


def main():
    """
    메인 애플리케이션 로직을 구현합니다.

    주요 구성 요소:
    1. 페이지 제목 및 기본 설정
    2. 세션 상태 초기화 및 관리
    3. 사이드바 필터 구현
    4. 컬럼 표시/숨김 설정
    5. 데이터 필터링 로직
    6. 테이블 표시 (편집/보기 모드)
    7. 통계 정보 표시

    Streamlit 위젯 사용법:
    - st.title(): 페이지 제목 설정
    - st.sidebar: 사이드바 영역 생성
    - st.selectbox: 드롭다운 선택 메뉴
    - st.multiselect: 다중 선택 메뉴
    - st.columns: 화면 분할
    - st.toggle: 켜기/끄기 스위치
    - st.data_editor: 편집 가능한 테이블
    - st.dataframe: 읽기 전용 테이블
    - st.button: 클릭 가능한 버튼
    """
    st.title("🔬 연구 프로젝트 관리 시스템")

    # 세션 상태 초기화
    if "data" not in st.session_state:
        st.session_state.data = load_data()
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False
    if st.session_state.data is None:
        return

    # 사이드바 필터 구현
    st.sidebar.header("필터")
    departments = ["전체"] + sorted(
        st.session_state.data["Department"].unique().tolist()
    )
    statuses = ["전체"] + sorted(st.session_state.data["Status"].unique().tolist())

    selected_dept = st.sidebar.selectbox("부서", departments)
    selected_status = st.sidebar.selectbox("상태", statuses)

    # 컬럼 관리
    st.sidebar.header("컬럼 설정")
    hide_columns = st.sidebar.multiselect(
        "숨길 컬럼 선택",
        options=st.session_state.data.columns.tolist(),
        default=[],
        format_func=lambda x: {
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

    # 데이터 필터링
    filtered_df = st.session_state.data.copy()
    if selected_dept != "전체":
        filtered_df = filtered_df[filtered_df["Department"] == selected_dept]
    if selected_status != "전체":
        filtered_df = filtered_df[filtered_df["Status"] == selected_status]

    display_columns = [
        col for col in st.session_state.data.columns if col not in hide_columns
    ]
    filtered_df = filtered_df[display_columns]

    # 편집 모드 토글
    col1, col2, col3 = st.columns([6, 2, 2])
    with col1:
        edit_mode = st.toggle("편집 모드", key="edit_toggle")

    # 테이블 표시
    if edit_mode:
        st.warning("⚠️ 변경사항을 저장하지 않으면 수정한 내용이 사라집니다.")
        edited_df = st.data_editor(
            filtered_df,
            column_config=get_column_config(is_edit_mode=True),
            use_container_width=True,
            num_rows="dynamic",
            height=500,
            hide_index=False,
        )

        with col3:
            if st.button("변경사항 저장", type="primary", use_container_width=True):
                for idx in filtered_df.index:
                    st.session_state.data.loc[idx] = edited_df.loc[idx]
                save_data(st.session_state.data)
                st.session_state.edit_mode = False
                st.rerun()
    else:
        st.dataframe(
            filtered_df,
            column_config=get_column_config(is_edit_mode=False),
            use_container_width=True,
            hide_index=False,
            height=500,
        )

    # 통계 정보 표시
    st.sidebar.markdown("---")
    st.sidebar.info("📊 현재 표시된 프로젝트 통계")
    st.sidebar.markdown(f"- 전체 프로젝트: {len(st.session_state.data)}개")
    st.sidebar.markdown(f"- 필터링된 프로젝트: {len(filtered_df)}개")


if __name__ == "__main__":
    main()
