import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="SCM CHINA INTELLIGENCE", layout="wide")

# 1. 초기 데이터 설정 (세션 상태를 이용해 데이터 유지)
if 'partners' not in st.session_state:
    st.session_state.partners = [
        { 
            "id": 1, "category": "생산업체", "name": "YINHE ALUMINUM", "alloy": "1xxx, 3xxx", 
            "temper": "O, H14, H18", "location": "중국 공이시", "contact": "Zhang Jie Jing", 
            "info": "+86 15290891059", "minWidth": 20, "maxWidth": 1880, "minThickness": 0.15, "maxThickness": 3.0 
        },
        { 
            "id": 2, "category": "유통상", "name": "GYJ ALUMINUM", "alloy": "1050, 1100, 3003", 
            "temper": "H18, O", "location": "중국 선전시", "contact": "Lily Tan", 
            "info": "+86 15813747894", "minWidth": 10, "maxWidth": 1600, "minThickness": 0.006, "maxThickness": 0.2 
        }
    ]

# 사이드바 - 신규 등록 폼
with st.sidebar:
    st.header("🆕 신규 업체 등록")
    with st.form("new_partner_form", clear_on_submit=True):
        new_name = st.text_input("업체명")
        new_cat = st.selectbox("카테고리", ["생산업체", "유통상", "구리/합금", "설비/공구"])
        new_alloy = st.text_input("알루미늄 재질 (Alloy)", placeholder="예: 1xxx, 3003")
        new_temper = st.text_input("조질 (Temper)", placeholder="예: O, H14, H18")
        new_loc = st.text_input("위치 (지역)")
        
        col1, col2 = st.columns(2)
        with col1:
            min_w = st.number_input("최소 폭 (mm)", value=0.0)
            min_t = st.number_input("최소 두께 (mm)", value=0.000, format="%.3f")
        with col2:
            max_w = st.number_input("최대 폭 (mm)", value=0.0)
            max_t = st.number_input("최대 두께 (mm)", value=0.000, format="%.3f")
            
        new_contact = st.text_input("담당자")
        new_info = st.text_input("연락처")
        
        submit = st.form_submit_button("업체 등록하기")
        
        if submit and new_name:
            new_data = {
                "id": int(datetime.now().timestamp()),
                "category": new_cat,
                "name": new_name,
                "alloy": new_alloy,
                "temper": new_temper,
                "location": new_loc,
                "contact": new_contact,
                "info": new_info,
                "minWidth": min_w,
                "maxWidth": max_w,
                "minThickness": min_t,
                "maxThickness": max_t
            }
            st.session_state.partners.append(new_data)
            st.success(f"{new_name} 등록 완료!")

# 메인 화면 구성
st.title("🌐 SCM CHINA INTELLIGENCE")
st.caption("Aluminum Supply Chain Management System (Python Version)")

# 검색 기능
search_query = st.text_input("🔍 업체명, 재질(Alloy), 또는 지역으로 검색하세요")

# 상단 탭 구성
tabs = st.tabs(["🏭 생산업체", "🚚 유통상", "🥉 구리/합금", "🛠️ 설비/공구"])

for i, tab_name in enumerate(["생산업체", "유통상", "구리/합금", "설비/공구"]):
    with tabs[i]:
        # 데이터 필터링
        filtered_data = [p for p in st.session_state.partners if p['category'] == tab_name]
        if search_query:
            q = search_query.lower()
            filtered_data = [p for p in filtered_data if q in p['name'].lower() or q in p['alloy'].lower() or q in p['location'].lower()]
        
        if not filtered_data:
            st.info(f"{tab_name} 카테고리에 등록된 업체가 없습니다.")
        else:
            # 업체 리스트 출력
            for item in filtered_data:
                with st.container():
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        st.subheader(f"{item['name']}")
                        st.markdown(f"📍 **위치:** {item['location']} | 🧪 **재질:** {item['alloy']}")
                    with c2:
                        st.button(f"수정", key=f"edit_{item['id']}")
                    
                    # 상세 스펙 표시 (Metric 사용)
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric("조질 (Temper)", item['temper'])
                    m2.metric("가용 폭", f"{item['minWidth']} ~ {item['maxWidth']} mm")
                    m3.metric("가용 두께", f"{item['minThickness']} ~ {item['maxThickness']} mm")
                    m4.write(f"👤 **담당자:** {item['contact']}\n\n📞 **연락처:** {item['info']}")
                    
                    st.divider()

# 데이터 테이블 보기 (원격 확인용)
with st.expander("📊 전체 데이터 원본 보기"):
    st.dataframe(pd.DataFrame(st.session_state.partners), use_container_width=True)