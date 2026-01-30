import streamlit as st
import pandas as pd

st.set_page_config(page_title="My Grade Dashboard", page_icon="📊", layout="wide")

st.title("📊 나만의 성적 관리 대시보드")

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["학년", "시험", "과목", "점수"])

if 'subject_list' not in st.session_state:
    st.session_state.subject_list = []

with st.sidebar:
    # 1. 시험 종류 먼저 선택 (가장 위)
    st.header("📅 시험 선택")
    grade = st.selectbox("학년", ["1학년", "2학년", "3학년"])
    exam_type = st.selectbox("시험 종류", ["1학기 중간", "1학기 기말", "2학기 중간", "2학기 기말"])
    
    st.divider()

    # 2. 과목 추가 및 관리
    st.header("📚 과목 관리")
    new_subject = st.text_input("새 과목 추가", placeholder="예: 국어, 수학")
    if st.button("과목 추가"):
        if new_subject and new_subject not in st.session_state.subject_list:
            st.session_state.subject_list.append(new_subject)
            st.rerun()

    if st.session_state.subject_list:
        with st.expander("과목 이름 수정 / 삭제"):
            for i, sub in enumerate(st.session_state.subject_list):
                cols = st.columns([2, 1])
                with cols[0]:
                    edited_name = st.text_input(f"수정 {i}", value=sub, label_visibility="collapsed", key=f"edit_{i}")
                    if edited_name != sub:
                        st.session_state.subject_list[i] = edited_name
                        st.session_state.data.loc[st.session_state.data["과목"] == sub, "과목"] = edited_name
                        st.rerun()
                with cols[1]:
                    if st.button("삭제", key=f"del_sub_{i}"):
                        st.session_state.subject_list.pop(i)
                        st.session_state.data = st.session_state.data[st.session_state.data["과목"] != sub]
                        st.
