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
                        st.rerun()

    # 3. 점수 입력
    if st.session_state.subject_list:
        st.divider()
        st.header(f"📝 {exam_type} 점수 입력")
        selected_scores = {}
        for sub in st.session_state.subject_list:
            # 해당 시험의 기존 점수가 있다면 불러오기
            existing_val = st.session_state.data[
                (st.session_state.data["학년"] == grade) & 
                (st.session_state.data["시험"] == exam_type) & 
                (st.session_state.data["과목"] == sub)
            ]["점수"]
            default_val = int(existing_val.iloc[0]) if not existing_val.empty else 0
            
            selected_scores[sub] = st.number_input(f"{sub} 점수", min_value=0, max_value=100, value=default_val, key=f"input_{sub}")
        
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

# 메인 화면 시각화 부분
if not st.session_state.data.empty:
    st.divider()
    col_header, col_chart_type = st.columns([3, 1])
    with col_header:
        st.subheader("📈 성적 시각화")
    with col_chart_type:
        chart_type = st.radio("그래프 선택", ["꺾은선", "막대"], horizontal=True)

    chart_df = st.session_state.data.copy()
    chart_df["시험명"] = chart_df["학년"] + " " + chart_df["시험"]
    
    # 시험 순서 정렬을 위해 피벗 테이블 생성
    chart_pivot = chart_df.pivot_table(index="시험명", columns="과목", values="점수", aggfunc='mean')
    
    if chart_type == "꺾은선":
        st.line_chart(chart_pivot)
    else:
        st.bar_chart(chart_pivot)

    st.subheader("📑 전체 성적표")
    display_df = st.session_state.data.pivot_table(index=["학년", "시험"], columns="과목", values="점수").reset_index()
    st.dataframe(display_df, use_container_width=True)

    if st.button("전체 데이터 초기화"):
        st.session_state.data = pd.DataFrame(columns=["학년", "시험", "과목", "점수"])
        st.session_state.subject_list = []
        st.rerun()
else:
    st.info("사이드바에서 시험을 선택하고 과목과 점수를 입력해 보세요!")
