import streamlit as st
import pandas as pd

st.set_page_config(page_title="My Goal Tracker", page_icon="🎯")
st.title("🎯 목표 달성 추적기")
st.markdown("나의 목표를 설정하고 한 걸음씩 나아가보세요!")

with st.sidebar:
    st.header("새로운 목표 설정")
    goal_name = st.text_input("목표 이름", placeholder="예: 파이썬 공부하기")
    target_value = st.number_input("최종 목표 수치", min_value=1, value=100)
    add_btn = st.button("목표 추가하기")

if 'goals' not in st.session_state:
    st.session_state.goals = []

if add_btn and goal_name:
    st.session_state.goals.append({
        "name": goal_name,
        "target": target_value,
        "current": 0
    })
    st.success(f"'{goal_name}' 목표가 생성되었습니다!")

if st.session_state.goals:
    st.divider()
    for i, goal in enumerate(st.session_state.goals):
        cols = st.columns([3, 2, 1])
        
        with cols[0]:
            st.subheader(goal['name'])
            
        with cols[1]:
            new_val = st.number_input(f"현재 진행도 ({goal['name']})", 
                                      min_value=0, 
                                      max_value=goal['target'], 
                                      value=goal['current'], 
                                      key=f"input_{i}")
            st.session_state.goals[i]['current'] = new_val
            
        with cols[2]:
            if st.button("삭제", key=f"del_{i}"):
                st.session_state.goals.pop(i)
                st.rerun()

        progress = goal['current'] / goal['target']
        st.progress(progress)
        st.write(f"달성률: {progress*100:.1f}% ({goal['current']} / {goal['target']})")
        
        if progress