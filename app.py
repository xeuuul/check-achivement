import streamlit as st
import pandas as pd

st.set_page_config(page_title="Grade Manager", page_icon="📈", layout="wide")
st.title("📈 성적 관리 대시보드")

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["학년", "시험", "과목", "점수"])

with st.sidebar:
    st.header("📝 점수 입력")
    grade = st.selectbox("학년", ["1학년", "2학년", "3학년"])
    exam_type = st.selectbox("시험 종류", ["1학기 중간", "1학기 기말", "2학기 중간", "2학기 기말"])
    
    st.divider()
    
    new_scores = {}
    subjects = ["국어", "수학", "영어", "과학", "사회"]
    for sub in subjects:
        new_scores[sub] = st.number_input(f"{sub} 점수", min_value=0, max_value=100, value=0, key=f"{grade}_{exam_type}_{sub}")
    
    add_btn = st.button("성적 기록하기")

if add_btn:
    for sub, score in new_scores.items():
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
    chart_data = st.session_state.data.pivot_table(index=["학년", "시험"], columns="과목", values="점수", aggfunc='first')
    
    # 에러 방지: 데이터가 유효할 때만 그래프 출력
    if not chart_data.empty:
        st.line_chart(chart_data)

    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📑 전체 성적표")
        pivot_df = st.session_state.data.pivot_table(index=["학년", "시험"], columns="과목", values="점수").reset_index()
        st.dataframe(pivot_df, use_container_width=True)

    with col2:
        st.subheader("🔢 과목별 평균 점수")
        avg_scores = st.session_state.data.groupby("과목")["점수"].mean().reset_index()
        st.table(avg_scores.style.format({"점수": "{:.1f}점"}))

    if st.button("데이터 초기화"):
        st.session_state.data = pd.DataFrame(columns=["학년", "시험", "과목", "점수"])
        st.rerun()
else:
    st.info("왼쪽 사이드바에서 성적을 입력하고 '성적 기록하기' 버튼을 눌러주세요.")
