import streamlit as st
import pandas as pd

st.set_page_config(page_title="My Grade Record", page_icon="📝", layout="wide")

st.title("📝 나만의 성적 기록장")
st.markdown("과목을 직접 추가하고 시험별 성적을 관리해보세요.")

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["학년", "시험", "과목", "점수"])

if 'subject_list' not in st.session_state:
    st.session_state.subject_list = []

with st.sidebar:
    st.header("📚 과목 관리")
    new_subject = st.text_input("새 과목 추가", placeholder="예: 코딩, 일본어")
    if st.button("과목 추가"):
        if new_subject and new_subject not in st.session_state.subject_list:
            st.session_state.subject_list.append(new_subject)
            st.success(f"'{new_subject}' 추가 완료!")
        elif new_subject in st.session_state.subject_list:
            st.warning("이미 추가된 과목입니다.")

    if st.session_state.subject_list:
        st.divider()
        st.header("📝 점수 입력")
        grade = st.selectbox("학년", ["1학년", "2학년", "3학년"])
        exam_type = st.selectbox("시험 종류", ["1학기 중간", "1학기 기말", "2학기 중간", "2학기 기말"])
        
        selected_scores = {}
        for sub in st.session_state.subject_list:
            selected_scores[sub] = st.number_input(f"{sub} 점수", min_value=0, max_value=100, value=0, key=f"{grade}_{exam_type}_{sub}")
        
        if st.button("성적 기록하기"):
            for sub, score in selected_scores.items():
                mask = (st.session_state.data["학년"] == grade) & \
                       (st.session_state.data["시험"] == exam_type) & \
                       (st.session_state.data["과목"] == sub)
                
                if any(mask):
                    st.session_state.data.loc[mask, "점수"] = score
                else:
                    new_row = pd.DataFrame({"학년": [grade], "시험": [exam_type], "과목": [sub], "점수": [score]})
                    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
            st.success(f"{grade} {exam_type} 성적이 저장되었습니다!")

if not st.session_state.data.empty:
    st.subheader("📊 과목별 성적 추이")
    
    chart_df = st.session_state.data.copy()
    chart_df["시험명"] = chart_df["학년"] + " " + chart_df["시험"]
    chart_pivot = chart_df.pivot(index="시험명", columns="과목", values="점수")
    
    if not chart_pivot.empty:
        st.line_chart(chart_pivot)

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📑 전체 성적표")
        display_df = st.session_state.data.pivot_table(index=["학년", "시험"], columns="과목", values="점수").reset_index()
        st.dataframe(display_df, use_container_width=True)

    with col2:
        st.subheader("🔢 과목별 평균 점수")
        avg_scores = st.session_state.data.groupby("과목")["점수"].mean().reset_index()
        st.table(avg_scores.style.format({"점수": "{:.1f}점"}))

    if st.button("전체 초기화"):
        st.session_state.data = pd.DataFrame(columns=["학년", "시험", "과목", "점수"])
        st.session_state.subject_list = []
        st.rerun()
else:
    if not st.session_state.subject_list:
        st.info("먼저 왼쪽 사이드바에서 과목을 추가해주세요!")
    else:
        st.info("과목 점수를 입력하고 '성적 기록하기'를 눌러주세요.")
