import streamlit as st
import pandas as pd

st.set_page_config(page_title="My Grade Dashboard", page_icon="📊", layout="wide")

st.title("📊 나만의 성적 관리 대시보드")
st.markdown("과목을 추가하고 시험 성적을 그래프로 비교해보세요.")

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["학년", "시험", "과목", "점수"])

if 'subject_list' not in st.session_state:
    st.session_state.subject_list = []

with st.sidebar:
    st.header("📚 과목 추가")
    new_subject = st.text_input("새 과목 입력", placeholder="예: 국어, 코딩")
    if st.button("과목 추가"):
        if new_subject and new_subject not in st.session_state.subject_list:
            st.session_state.subject_list.append(new_subject)
            st.success(f"'{new_subject}' 추가됨!")
        elif new_subject in st.session_state.subject_list:
            st.warning("이미 있는 과목입니다.")

    if st.session_state.subject_list:
        st.divider()
        st.header("📝 성적 기록")
        grade = st.selectbox("학년", ["1학년", "2학년", "3학년"])
        exam_type = st.selectbox("시험 종류", ["1학기 중간", "1학기 기말", "2학기 중간", "2학기 기말"])
        
        selected_scores = {}
        for sub in st.session_state.subject_list:
            selected_scores[sub] = st.number_input(f"{sub} 점수", min_value=0, max_value=100, value=0, key=f"{grade}_{exam_type}_{sub}")
        
        if st.button("성적 저장"):
            for sub, score in selected_scores.items():
                mask = (st.session_state.data["학년"] == grade) & \
                       (st.session_state.data["시험"] == exam_type) & \
                       (st.session_state.data["과목"] == sub)
                
                if any(mask):
                    st.session_state.data.loc[mask, "점수"] = score
                else:
                    new_row = pd.DataFrame({"학년": [grade], "시험": [exam_type], "과목": [sub], "점수": [score]})
                    st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
            st.success(f"{grade} {exam_type} 저장 완료!")

if not st.session_state.data.empty:
    st.divider()
    
    col_header, col_chart_type = st.columns([3, 1])
    with col_header:
        st.subheader("📈 성적 시
