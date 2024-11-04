import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from config import DATA_PATH


def generate_research_data(n_projects=50):
    current_date = datetime.now()

    # 상수 정의
    INVESTIGATORS = [
        "김지원",
        "이성민",
        "박도현",
        "정수진",
        "최영호",
        "강민서",
        "윤지현",
        "송태호",
        "임하늘",
        "한소희",
    ]
    DEPARTMENTS = [
        "생명과학부",
        "물리학과",
        "화학과",
        "컴퓨터공학과",
        "전자공학과",
        "기계공학과",
        "의학과",
        "약학과",
    ]
    RESEARCH_AREAS = [
        "인공지능",
        "신약개발",
        "재생에너지",
        "나노기술",
        "로보틱스",
        "바이오테크",
        "양자컴퓨팅",
        "신소재",
    ]
    STATUSES = ["진행중", "완료", "중단", "검토중", "준비중"]
    PHASES = ["계획", "실험", "데이터수집", "분석", "검증", "논문작성", "특허출원"]

    data = {
        "Project_ID": [f"PRJ-{str(i).zfill(3)}" for i in range(1, n_projects + 1)],
        "Project_Name": [f"Research Project {i}" for i in range(1, n_projects + 1)],
        "Principal_Investigator": [
            np.random.choice(INVESTIGATORS) for _ in range(n_projects)
        ],
        "Department": [np.random.choice(DEPARTMENTS) for _ in range(n_projects)],
        "Start_Date": [
            (current_date - timedelta(days=np.random.randint(0, 365))).strftime(
                "%Y-%m-%d"
            )
            for _ in range(n_projects)
        ],
        "End_Date": [
            (current_date + timedelta(days=np.random.randint(30, 730))).strftime(
                "%Y-%m-%d"
            )
            for _ in range(n_projects)
        ],
        "Budget": [np.random.randint(5000, 50000) * 10000 for _ in range(n_projects)],
        "Progress": [np.random.randint(0, 101) for _ in range(n_projects)],
        "Research_Area": [np.random.choice(RESEARCH_AREAS) for _ in range(n_projects)],
        "Status": [np.random.choice(STATUSES) for _ in range(n_projects)],
        "Current_Phase": [np.random.choice(PHASES) for _ in range(n_projects)],
        "Review_Comments": [""] * n_projects,
        "Action_Items": [""] * n_projects,
    }

    df = pd.DataFrame(data)

    try:
        df.to_csv(DATA_PATH, index=False, encoding="utf-8-sig")
        print(f"데이터가 성공적으로 생성되었습니다: {DATA_PATH}")
        return df
    except Exception as e:
        print(f"데이터 저장 중 오류가 발생했습니다: {str(e)}")
        return None


if __name__ == "__main__":
    generate_research_data()
