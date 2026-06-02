# -*- coding: utf-8 -*-
"""
위스키 프리미엄 가격 가이드 웹 서비스 (WhiskyPrice Premium)
메인 애플리케이션 파일
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from database import (
    WHISKY_DATA,
    get_whisky_dataframe,
    get_categories,
    get_origins,
    search_whisky,
    get_whisky_by_id,
    recommend_whiskies,
    get_whisky_image_url
)
from styles import apply_premium_styles, premium_card_html

# 페이지 기본 설정
st.set_page_config(
    page_title="WhiskyPrice Premium | 위스키 가격 가이드",
    page_icon="🥃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 고급 커스텀 스타일링 주입
apply_premium_styles()

# ----------------- 사이드바 영역 -----------------
st.sidebar.markdown(
    """
    <div style="text-align:center; padding: 15px 0;">
        <h2 style="font-family:'Cinzel', serif; color:#dfba6b; margin:0; font-size:1.8rem;">BARRIQUE</h2>
        <p style="font-size:0.75rem; color:#8e8270; margin-top:2px; letter-spacing:2px; font-weight:300;">PREMIUM GUIDE</p>
    </div>
    <hr style="margin: 10px 0 !important;">
    """,
    unsafe_allow_html=True
)

st.sidebar.subheader("📋 위스키 정렬 및 필터")
sort_option = st.sidebar.selectbox(
    "정렬 기준",
    ["이름순 (가나다)", "가격 낮은 순", "가격 높은 순", "도수 높은 순"]
)

st.sidebar.markdown(
    """
    <hr style="margin: 15px 0 !important;">
    <div style="background-color: #1a1410; padding: 15px; border-radius: 8px; border: 1px solid #3d2f25;">
        <h4 style="color:#dfba6b; margin-top:0; font-size:0.95rem; font-family:'Inter', sans-serif;">💡 이용 팁</h4>
        <p style="font-size:0.8rem; color:#c7b9a5; line-height:1.6; margin-bottom:0;">
            1. <b>상세 탐색</b> 탭에서 위스키를 클릭하시면 맛 분석 레이더 차트와 채널별 가격 비교 차트가 나타납니다.<br>
            2. 직구 계획이 있으시다면 <b>스마트 계산기</b>에서 주세, 교육세, 부가세를 정확히 미리 시뮬레이션해 보세요!
        </p>
    </div>
    <div style="text-align:center; margin-top: 30px; font-size:0.75rem; color:#5c5043;">
        © 2026 Barrique Premium. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------- 메인 타이틀 배너 -----------------
st.markdown(
    """
    <div class="premium-banner">
        <h1 class="premium-title">WHISKYPRICE PREMIUM</h1>
        <p class="premium-subtitle">현명한 위스키 애호가를 위한 고품격 가격 비교 & 맛 가이드</p>
    </div>
    """,
    unsafe_allow_html=True
)

# 데이터 준비
df_raw = get_whisky_dataframe()

# 정렬 로직 적용
if sort_option == "이름순 (가나다)":
    df_sorted = df_raw.sort_values(by="name_ko")
elif sort_option == "가격 낮은 순":
    # 정렬용 가격 추출 helper 함수
    df_raw['sort_price'] = df_raw['current_prices'].apply(lambda x: x.get('대형마트/스마트오더', 0))
    df_sorted = df_raw.sort_values(by="sort_price", ascending=True)
elif sort_option == "가격 높은 순":
    df_raw['sort_price'] = df_raw['current_prices'].apply(lambda x: x.get('대형마트/스마트오더', 0))
    df_sorted = df_raw.sort_values(by="sort_price", ascending=False)
elif sort_option == "도수 높은 순":
    df_sorted = df_raw.sort_values(by="abv", ascending=False)

# 위스키 목록 리스트 재구성
whisky_list = df_sorted.to_dict('records')

# ----------------- 메인 멀티 탭 구성 -----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🥃 홈 & 인기 대시보드",
    "🔍 위스키 상세 탐색",
    "📈 가격 트렌드 분석",
    "🎯 취향 맞춤 추천",
    "🧮 스마트 계산기"
])

# ================= TAB 1: 홈 & 인기 대시보드 =================
with tab1:
    st.markdown("### 🏆 오늘의 스마트 리포트")
    
    # 상단 요약 메트릭스
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("총 등록 위스키", f"{len(WHISKY_DATA)}종")
    with col2:
        # 싱글몰트 비율
        sm_count = len([w for w in WHISKY_DATA if w['category'] == '싱글몰트'])
        st.metric("싱글몰트 점유율", f"{round(sm_count/len(WHISKY_DATA)*100, 1)}%")
    with col3:
        # 평균 대형마트 가격
        prices = [w['current_prices']['대형마트/스마트오더'] for w in WHISKY_DATA]
        avg_price = int(np.mean(prices))
        st.metric("마트 평균 소매가", f"{avg_price:,}원")
    with col4:
        st.metric("최고 도수 위스키", f"50.5% (와일드 터키)")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 2열 레이아웃: 에디터스 픽 및 가성비 추천
    left_col, right_col = st.columns([3, 2])
    
    with left_col:
        st.markdown("### ✨ 에디터 추천 프리미엄 위스키 3선")
        st.markdown("<p style='font-size:0.9rem; color:#a0907a; margin-top:-10px;'>테이스팅 노트와 입문 만족도가 매우 훌륭한 최고의 대표 상품입니다.</p>", unsafe_allow_html=True)
        
        # 대표 추천 위스키 3종 추출 (맥캘란 12셰리, 발베니 12더블, 야마자키 12)
        picks = ["macallan_12_sherry", "balvenie_12_doublewood", "yamazaki_12"]
        picked_whiskies = [w for w in WHISKY_DATA if w['id'] in picks]
        
        pick_cols = st.columns(3)
        for i, w in enumerate(picked_whiskies):
            with pick_cols[i]:
                with st.container(border=True):
                    st.image(get_whisky_image_url(w), use_container_width=True)
                    st.markdown(f"#### {w['name_ko']}")
                    st.markdown(f"<p style='color:#a89984; font-size:0.8rem; margin-top:-10px; font-style:italic;'>{w['name_en']} ({w['abv']}% / {w['age']}Y)</p>", unsafe_allow_html=True)
                    st.markdown(f"<span class='category-badge'>{w['category']}</span><span class='origin-badge'>{w['origin']}</span>", unsafe_allow_html=True)
                    st.write(w['description'])
                    st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center; margin-top:15px; padding-top:10px; border-top:1px solid #2b1f15;'><span style='font-size:0.8rem; color:#8e8270;'>마트 평균가</span><span style='font-size:1.15rem; font-weight:700; color:#dfba6b;'>{w['current_prices']['대형마트/스마트오더']:,}원</span></div>", unsafe_allow_html=True)
                
    with right_col:
        st.markdown("### 🟢 현재 가장 저렴해진 가성비 위스키")
        st.markdown("<p style='font-size:0.9rem; color:#a0907a; margin-top:-10px;'>1년 전 가격 고점 대비 현재 가격이 가장 합리적인 가성비 추천작입니다.</p>", unsafe_allow_html=True)
        
        # 12개월 전 가격 대비 현재 가격 하락율이 가장 높은 3종 선정
        bargain_whiskies = []
        for w in WHISKY_DATA:
            hist = w['price_history']
            current = w['current_prices']['대형마트/스마트오더']
            peak = max(hist)
            drop_rate = ((peak - current) / peak) * 100 if peak > 0 else 0
            bargain_whiskies.append((w, drop_rate, peak, current))
            
        bargain_whiskies.sort(key=lambda x: x[1], reverse=True)
        
        for w, rate, peak, current in bargain_whiskies[:3]:
            st.markdown(
                f"""
                <div style="background-color: #1e1610; padding: 15px; border-radius: 8px; border-left: 4px solid #4caf50; margin-bottom: 12px; border-top: 1px solid #3d2f25; border-right: 1px solid #3d2f25; border-bottom: 1px solid #3d2f25;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="font-weight:600; color:#dfba6b; font-size:1rem;">{w['name_ko']}</span>
                        <span style="background-color:#1b5e20; color:#81c784; border-radius:4px; padding: 1px 6px; font-size:0.75rem; font-weight:bold;">-{round(rate, 1)}% Down</span>
                    </div>
                    <p style="font-size:0.75rem; color:#a89984; margin: 3px 0 8px 0;">{w['name_en']}</p>
                    <div style="display:flex; justify-content:space-between; font-size:0.85rem; color:#ebd9c2;">
                        <span>최고가: <del>{peak:,}원</del></span>
                        <span style="font-weight:bold; color:#81c784;">현재가: {current:,}원</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
        # 위스키 테이스팅 기본 지식 카드
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <div style="background: linear-gradient(135deg, #1b1612 0%, #100a06 100%); padding: 20px; border-radius: 10px; border: 1px solid #4a382c;">
                <h4 style="font-family:'Cinzel', serif; color:#dfba6b; margin-top:0;">📝 마스터의 위스키 음용법 가이드</h4>
                <p style="font-size:0.82rem; color:#ebd9c2; line-height:1.6; margin-bottom:0;">
                    <b>1. 니트 (Neat)</b>: 얼음 없이 잔에 위스키 원액만 담아 본연의 향을 음미합니다.<br>
                    <b>2. 온더락 (On the Rocks)</b>: 커다란 얼음을 넣어 녹여가며 도수를 부드럽게 씻어내어 마십니다.<br>
                    <b>3. 하이볼 (Highball)</b>: 탄산수나 토닉워터, 레몬을 믹싱하여 캐주얼하게 즐깁니다. (제임슨, 버팔로 트레이스 강력 추천)
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ================= TAB 2: 위스키 상세 탐색 =================
with tab2:
    st.markdown("### 🔍 위스키 프리미엄 쇼룸")
    st.markdown("<p style='font-size:0.9rem; color:#a0907a; margin-top:-10px;'>원하시는 위스키를 다각도 조건으로 필터링하고 맛과 가격 정보를 한눈에 분석해 보세요.</p>", unsafe_allow_html=True)
    
    # 다차원 검색 필터 레이아웃
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    
    with f_col1:
        search_keyword = st.text_input("위스키 이름 검색", placeholder="예: 맥캘란, 발베니, 조니워커...")
        
    with f_col2:
        categories = ["전체"] + get_categories()
        selected_category = st.selectbox("카테고리 선택", categories)
        
    with f_col3:
        origins = ["전체"] + get_origins()
        selected_origin = st.selectbox("원산지 선택", origins)
        
    with f_col4:
        min_p = min(prices)
        max_p = max(prices)
        price_range = st.slider(
            "대형마트 예산대 설정 (원)",
            min_value=int(min_p),
            max_value=int(max_p),
            value=(int(min_p), int(max_p)),
            step=10000
        )
        
    # 필터링 적용
    filtered_whiskies = whisky_list
    
    if search_keyword:
        search_keyword = search_keyword.lower()
        filtered_whiskies = [w for w in filtered_whiskies if search_keyword in w["name_ko"].lower() or search_keyword in w["name_en"].lower()]
        
    if selected_category != "전체":
        filtered_whiskies = [w for w in filtered_whiskies if w["category"] == selected_category]
        
    if selected_origin != "전체":
        filtered_whiskies = [w for w in filtered_whiskies if selected_origin in w["origin"]]
        
    filtered_whiskies = [w for w in filtered_whiskies if price_range[0] <= w["current_prices"]["대형마트/스마트오더"] <= price_range[1]]
    
    st.markdown(f"<p style='font-size:0.85rem; color:#dfba6b;'>🔍 검색 결과: <b>{len(filtered_whiskies)}</b>종의 위스키가 매칭되었습니다.</p>", unsafe_allow_html=True)
    
    if not filtered_whiskies:
        st.warning("설정한 필터 조건과 일치하는 위스키가 없습니다. 필터를 완화해 보세요.")
    else:
        # Grid 레이아웃으로 위스키 카드 노출
        # 한 줄에 3개씩 배치
        cols_per_row = 3
        for r in range(0, len(filtered_whiskies), cols_per_row):
            row_items = filtered_whiskies[r : r + cols_per_row]
            cols = st.columns(cols_per_row)
            for idx, w in enumerate(row_items):
                with cols[idx]:
                    with st.container(border=True):
                        st.image(get_whisky_image_url(w), use_container_width=True)
                        st.markdown(f"#### {w['name_ko']}")
                        st.markdown(f"<p style='color:#a89984; font-size:0.8rem; margin-top:-10px; font-style:italic;'>{w['name_en']} ({w['abv']}% / {w['age']}Y)</p>", unsafe_allow_html=True)
                        st.markdown(f"<span class='category-badge'>{w['category']}</span><span class='origin-badge'>{w['origin']}</span>", unsafe_allow_html=True)
                        # 고정 높이 설명 글
                        st.markdown(f"<div style='height: 80px; overflow: hidden; font-size:0.85rem; color:#ebd9c2; line-height:1.5; margin-bottom:10px;'>{w['description']}</div>", unsafe_allow_html=True)
                        
                        st.markdown(f"<div style='display:flex; justify-content:space-between; align-items:center; margin-top:10px; padding-top:10px; border-top:1px solid #2b1f15; margin-bottom:15px;'><span style='font-size:0.8rem; color:#8e8270;'>마트 평균가</span><span style='font-size:1.15rem; font-weight:700; color:#dfba6b;'>{w['current_prices']['대형마트/스마트오더']:,}원</span></div>", unsafe_allow_html=True)
                        
                        # 상세 분석을 열 수 있는 버튼
                        if st.button(f"📊 {w['name_ko']} 심층 분석", key=f"btn_detail_{w['id']}", use_container_width=True):
                            st.session_state['selected_whisky_id'] = w['id']
                            st.success(f"아래 [🔬 {w['name_ko']} 심층 분석 센터]로 데이터가 로드되었습니다!")
                        
        # 심층 분석 센터 (사용자가 버튼을 클릭한 경우 활성화)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 🔬 위스키 심층 분석 센터")
        
        # 선택된 위스키 세션 상태 유지
        if 'selected_whisky_id' not in st.session_state:
            st.session_state['selected_whisky_id'] = WHISKY_DATA[0]['id']
            
        selected_w = get_whisky_by_id(st.session_state['selected_whisky_id'])
        
        if selected_w:
            st.markdown(f"#### 🥃 [{selected_w['category']}] {selected_w['name_ko']} 상세 프로필 리포트")
            
            d_col1, d_col2 = st.columns([1, 1])
            
            with d_col1:
                st.markdown("##### 👅 오감 테이스팅 노트")
                notes = selected_w['tasting_notes']
                st.markdown(
                    f"""
                    <div class="tasting-note-box">
                        <div class="note-title">👃 Nose (향)</div>
                        <div style="color:#f5f2eb; margin-bottom:10px;">{notes['Nose']}</div>
                        
                        <div class="note-title">👅 Palate (맛)</div>
                        <div style="color:#f5f2eb; margin-bottom:10px;">{notes['Palate']}</div>
                        
                        <div class="note-title">🏁 Finish (여운)</div>
                        <div style="color:#f5f2eb;">{notes['Finish']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # 채널별 가격 비교 차트 (Plotly Bar Chart)
                st.markdown("##### 💵 유통 채널별 가격 현황")
                price_dict = selected_w['current_prices']
                price_df = pd.DataFrame({
                    "채널": list(price_dict.keys()),
                    "가격 (원)": list(price_dict.values())
                })
                
                fig_price = px.bar(
                    price_df,
                    x="채널",
                    y="가격 (원)",
                    text="가격 (원)",
                    color="가격 (원)",
                    color_continuous_scale=[[0, '#3d2f25'], [1, '#dfba6b']]
                )
                fig_price.update_traces(texttemplate='%{text:,}원', textposition='outside')
                fig_price.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='#ebd9c2',
                    xaxis_title=None,
                    yaxis_title=None,
                    height=280,
                    margin=dict(l=10, r=10, t=10, b=10)
                )
                fig_price.update_yaxes(showgrid=True, gridcolor='#221a14')
                st.plotly_chart(fig_price, use_container_width=True, config={'displayModeBar': False})
                
            with d_col2:
                st.markdown("##### 📊 맛 프로필 오각형 분석")
                
                profile_dict = selected_w['taste_profile']
                # 레이더 차트 데이터프레임 구성
                radar_df = pd.DataFrame({
                    "맛 특성": list(profile_dict.keys()),
                    "점수 (10점 만점)": list(profile_dict.values())
                })
                
                # Radar Chart 생성
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=list(profile_dict.values()) + [list(profile_dict.values())[0]],
                    theta=list(profile_dict.keys()) + [list(profile_dict.keys())[0]],
                    fill='toself',
                    fillcolor='rgba(223, 186, 107, 0.25)',
                    line=dict(color='#dfba6b', width=2),
                    name=selected_w['name_ko']
                ))
                
                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 10],
                            gridcolor='#3d2f25',
                            linecolor='#3d2f25',
                            tickfont=dict(color='#a0907a')
                        ),
                        angularaxis=dict(
                            gridcolor='#3d2f25',
                            linecolor='#3d2f25',
                            tickfont=dict(color='#ebd9c2', size=11)
                        ),
                        bgcolor='rgba(0,0,0,0)'
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False,
                    height=350,
                    margin=dict(l=50, r=50, t=30, b=30)
                )
                st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
                
                # 설명 코멘트 박스
                st.markdown(
                    f"""
                    <div style="background-color: #16120e; padding: 15px; border-radius: 8px; border: 1px solid #32251a; font-size:0.85rem; color:#c7b9a5; line-height: 1.6;">
                        🎯 <b>테이스팅 어드바이스:</b><br>
                        이 위스키는 <b>{max(profile_dict, key=profile_dict.get)}</b> 속성이 가장 도드라집니다. 
                        원산지는 <b>{selected_w['origin']}</b>이며, 스펙상 알코올 도수는 <b>{selected_w['abv']}%</b>입니다. 
                        가장 합리적으로 구매할 수 있는 채널은 <b>{min(price_dict, key=price_dict.get)}</b> 채널이며, 
                        현재 최저 판매가는 약 <b>{min(price_dict.values()):,}원</b>선입니다.
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ================= TAB 3: 가격 트렌드 분석 =================
with tab3:
    st.markdown("### 📈 가격 변동 트렌드 분석기")
    st.markdown("<p style='font-size:0.9rem; color:#a0907a; margin-top:-10px;'>최근 12개월간의 소매점 소매가 시세 추이를 확인하고, 스마트 신호등을 통해 지금 구매하는 것이 유리한지 분석합니다.</p>", unsafe_allow_html=True)
    
    t_col1, t_col2 = st.columns([1, 3])
    
    with t_col1:
        # 트렌드 분석 대상 위스키 선택
        trend_whisky_ko = st.selectbox("분석 대상 위스키", [w['name_ko'] for w in WHISKY_DATA])
        trend_w = next(w for w in WHISKY_DATA if w['name_ko'] == trend_whisky_ko)
        
        # 선택된 위스키 기본 정보 카드
        st.markdown(
            f"""
            <div style="background-color: #1a1410; padding: 15px; border-radius: 8px; border: 1px solid #3d2f25; margin-top:15px;">
                <p style="font-size:0.75rem; color:#dfba6b; font-weight:600; margin:0;">SELECTED BRAND</p>
                <h4 style="margin:5px 0; color:#ebd9c2; font-family:'Inter', sans-serif;">{trend_w['name_ko']}</h4>
                <p style="font-size:0.8rem; color:#a89984; margin:0 0 10px 0; font-style:italic;">{trend_w['name_en']}</p>
                <div style="font-size:0.85rem; color:#ebd9c2; line-height:1.7;">
                    • 카테고리: {trend_w['category']}<br>
                    • 알코올 도수: {trend_w['abv']}%<br>
                    • 현재 마트가격: {trend_w['current_prices']['대형마트/스마트오더']:,}원
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 스마트 신호등 로직
        hist = trend_w['price_history']
        avg_hist = int(np.mean(hist))
        current_price = trend_w['current_prices']['대형마트/스마트오더']
        diff = current_price - avg_hist
        diff_pct = (diff / avg_hist) * 100
        
        st.markdown("<br>", unsafe_allow_html=True)
        if diff_pct < -3.0:
            st.markdown(
                f"""
                <div style="background-color:#1c351f; border-left:5px solid #2e7d32; padding:15px; border-radius:8px;">
                    <div style="font-size:1.5rem; display:inline-block; margin-bottom:5px;">🟢 <b>매수 추천</b></div>
                    <p style="font-size:0.82rem; color:#a5d6a7; margin:0; line-height:1.5;">
                        현재 가격({current_price:,}원)이 최근 12개월 평균가({avg_hist:,}원)보다 <b>{abs(round(diff_pct, 1))}% 더 저렴</b>합니다! 구매하기에 매우 합리적인 시기입니다.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        elif diff_pct > 3.0:
            st.markdown(
                f"""
                <div style="background-color:#3e1c1c; border-left:5px solid #c62828; padding:15px; border-radius:8px;">
                    <div style="font-size:1.5rem; display:inline-block; margin-bottom:5px;">🔴 <b>구매 대기</b></div>
                    <p style="font-size:0.82rem; color:#ef9a9a; margin:0; line-height:1.5;">
                        현재 가격({current_price:,}원)이 최근 12개월 평균가({avg_hist:,}원)보다 <b>{round(diff_pct, 1)}% 비쌉니다</b>. 시세 조정을 기다리시거나 면세점 및 리커숍 채널을 찾아보는 것을 권장합니다.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="background-color:#352f1c; border-left:5px solid #f9a825; padding:15px; border-radius:8px;">
                    <div style="font-size:1.5rem; display:inline-block; margin-bottom:5px;">🟡 <b>구매 보통</b></div>
                    <p style="font-size:0.82rem; color:#ffe082; margin:0; line-height:1.5;">
                        현재 가격({current_price:,}원)이 최근 12개월 평균가({avg_hist:,}원)와 <b>유사한 수준</b>입니다. 평이한 시세이므로 기호에 따라 필요할 때 구매하셔도 좋습니다.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    with t_col2:
        # 시계열 가격 데이터 프레임 구성
        months = ["1년 전", "11개월 전", "10개월 전", "9개월 전", "8개월 전", "7개월 전", "6개월 전", "5개월 전", "4개월 전", "3개월 전", "지난달", "이번달"]
        trend_df = pd.DataFrame({
            "시점": months,
            "소매 가격 (원)": hist
        })
        
        # Plotly Line Chart 생성
        fig_line = go.Figure()
        
        fig_line.add_trace(go.Scatter(
            x=months,
            y=hist,
            mode='lines+markers',
            line=dict(color='#dfba6b', width=3),
            marker=dict(size=8, color='#b8860b', symbol='diamond'),
            hovertemplate='%{x}: <b>%{y:,}원</b><extra></extra>',
            fill='tozeroy',
            fillcolor='rgba(184, 134, 11, 0.05)'
        ))
        
        # 12개월 평균 수평선 추가
        fig_line.add_shape(
            type="line",
            x0=0,
            y0=avg_hist,
            x1=len(months)-1,
            y1=avg_hist,
            line=dict(color="#a0907a", width=1.5, dash="dash"),
            name="12개월 평균"
        )
        
        fig_line.add_annotation(
            x=months[1],
            y=avg_hist,
            text=f"12개월 평균가: {avg_hist:,}원",
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-15,
            font=dict(color="#c7b9a5", size=10),
            bgcolor="#1a1410"
        )
        
        fig_line.update_layout(
            title=dict(
                text=f"📊 {trend_w['name_ko']} 최근 12개월 평균 소매 시세 변동 흐름",
                font=dict(family='Inter', size=14, color='#dfba6b')
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(26, 20, 16, 0.3)',
            font_color='#ebd9c2',
            xaxis=dict(showgrid=False),
            yaxis=dict(
                showgrid=True,
                gridcolor='#2b1f15',
                tickformat=',원'
            ),
            height=400,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        
        st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
        
        # 분석 요약 텍스트
        st.markdown(
            f"""
            <div style="background-color: #130f0c; padding: 20px; border-radius: 8px; border: 1px solid #2b1f15; margin-top:15px;">
                <h5 style="color:#dfba6b; margin-top:0;">📊 데이터 심층 분석 코멘트</h5>
                <p style="font-size:0.85rem; color:#ebd9c2; line-height:1.6; margin-bottom:0;">
                    해당 제품의 12개월 최고 소매가는 <b>{max(hist):,}원</b>(1년 전 시점)이었으며, 최저 소매가는 <b>{min(hist):,}원</b>선이었습니다. 
                    시장 내 공급 안정화 및 유통 채널 다양화로 인해 전체적인 가격 동향은 안정적인 추세를 유지하고 있습니다. 
                    현재 가격은 평균선 대비 변동 폭이 크지 않은 안정적 구간에 진입해 있습니다.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ================= TAB 4: 취향 맞춤 추천 =================
with tab4:
    st.markdown("### 🎯 내 취향 저격 위스키 매칭 엔진")
    st.markdown("<p style='font-size:0.9rem; color:#a0907a; margin-top:-10px;'>내가 선호하는 맛 프로필과 예산을 슬라이더로 조절하시면, 정확도 매칭 스코어를 계산하여 최적의 위스키를 골라드립니다.</p>", unsafe_allow_html=True)
    
    rec_col1, rec_col2 = st.columns([1, 2])
    
    with rec_col1:
        st.markdown("##### ⚙️ 선호 취향 프로파일러")
        
        pref_sweetness = st.slider("단맛 선호도 (바닐라/캐러멜)", 1, 10, 5, help="점수가 높을수록 달콤한 풍미와 캐러멜 향이 진한 위스키를 추천합니다.")
        pref_peat = st.slider("피트 스모키 선호도 (약전/소독약/연기)", 1, 10, 1, help="피트 특유의 소독약 향이나 훈연 향을 선호하시면 높은 점수를 선택하세요.")
        pref_sherry = st.slider("셰리/과일향 선호도 (건자두/베리류)", 1, 10, 5, help="와인 오크통 특유의 화사하고 묵직한 건과일 풍미를 원하시면 높은 점수를 선택하세요.")
        pref_oak = st.slider("오크/나무향 선호도 (시나몬/가죽/스파이스)", 1, 10, 5, help="그을린 나무나 가죽, 알싸한 후추 향의 정도를 선택하세요.")
        pref_body = st.slider("바디감 선호도 (묵직함/입안의 질감)", 1, 10, 5, help="입안에서 느껴지는 바디감의 두터운 질감 정도를 뜻합니다.")
        
        max_budget = st.slider("최대 예산 한도 (원)", 30000, 400000, 200000, step=10000, format="%d원")
        
        st.markdown("<br>", unsafe_allow_html=True)
        rec_button = st.button("🔥 취향 매칭 시작하기")
        
    with rec_col2:
        st.markdown("##### 🏆 매칭 추천 위스키 TOP 3 결과")
        
        # 세션 상태나 버튼 클릭 시 매칭 계산
        user_prefs = {
            'Sweetness': pref_sweetness,
            'Peat': pref_peat,
            'Sherry': pref_sherry,
            'Oak': pref_oak,
            'Body': pref_body,
            'MaxPrice': max_budget
        }
        
        recommended = recommend_whiskies(user_prefs, limit=3)
        
        if not recommended:
            st.error("예산 한도 내에서 조건을 만족하는 위스키를 찾을 수 없습니다. 예산을 조금 늘려보세요.")
        else:
            for idx, item in enumerate(recommended):
                whisky = item['whisky']
                score = item['match_score']
                
                # 순위에 따라 왕관/뱃지 디자인 변경
                medal = "🥇 1위 추천" if idx == 0 else "🥈 2위 추천" if idx == 1 else "🥉 3위 추천"
                color_class = "#ffd700" if idx == 0 else "#c0c0c0" if idx == 1 else "#cd7f32"
                
                with st.container(border=True):
                    # 상단 점수 및 메달 정보
                    st.markdown(
                        f"""
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                            <span style="font-weight:700; color:{color_class}; border-bottom: 2px solid {color_class}; padding-bottom:3px; font-size:0.95rem;">{medal}</span>
                            <span style="font-size:1.2rem; font-weight:bold; color:#dfba6b;">{score}% 일치</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.image(get_whisky_image_url(whisky), use_container_width=True)
                    st.markdown(f"#### {whisky['name_ko']}")
                    st.markdown(f"<p style='color:#a89984; font-size:0.8rem; margin-top:-10px; font-style:italic;'>{whisky['name_en']} ({whisky['abv']}% / {whisky['age']}Y)</p>", unsafe_allow_html=True)
                    st.write(whisky['description'])
                    
                    st.markdown(
                        f"""
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:15px; padding-top:10px; border-top:1px solid #2b1f15; font-size:0.85rem;">
                            <span style="color:#a0907a;">생산국: <b>{whisky['origin']}</b></span>
                            <span style="color:#dfba6b; font-weight:bold; font-size:1.05rem;">마트 평균가 {whisky['current_prices']['대형마트/스마트오더']:,}원</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


# ================= TAB 5: 스마트 계산기 =================
with tab5:
    st.markdown("### 🧮 위스키 스마트 유틸리티 계산기")
    st.markdown("<p style='font-size:0.9rem; color:#a0907a; margin-top:-10px;'>해외 직구 시 예상되는 정확한 관부가세 세금 모의계산 및 모임용 바이알 분할가 계산을 지원합니다.</p>", unsafe_allow_html=True)
    
    calc_tab1, calc_tab2 = st.tabs([
        "✈️ 해외 직구 관부가세 계산기",
        "🧪 바이알(Vial) 분할 소분단가 계산기"
    ])
    
    # ✈️ 해외 직구 관부가세 계산기
    with calc_tab1:
        st.markdown("##### ✈️ 해외 직구 세금 시뮬레이션")
        st.markdown("<p style='font-size:0.8rem; color:#a0907a;'>현행 대한민국 세법에 근거한 주류 관세, 주세, 교육세, 부가세를 산정합니다. (1병 1.0L 이하 면세 규정 제외 기준)</p>", unsafe_allow_html=True)
        
        tax_col1, tax_col2 = st.columns([1, 1.2])
        
        with tax_col1:
            product_price_usd = st.number_input("위스키 상품가 ($ USD)", min_value=0.0, value=120.0, step=5.0)
            shipping_usd = st.number_input("해외 배송비 ($ USD)", min_value=0.0, value=35.0, step=5.0)
            exchange_rate = st.number_input("기준 환율 (원/$)", min_value=500.0, max_value=2500.0, value=1380.0, step=10.0)
            bottle_volume = st.number_input("주류 용량 (L리터, 예: 700ml = 0.7)", min_value=0.1, max_value=5.0, value=0.7, step=0.05)
            abv_input = st.number_input("알코올 도수 (%)", min_value=1.0, max_value=99.0, value=40.0, step=0.5)
            
            st.markdown(
                """
                <div style="background-color:#1a1410; padding:12px; border-radius:6px; border:1px solid #3d2f25; font-size:0.78rem; color:#a0907a; margin-top:15px;">
                    📝 <b>직구 세금 산정 기준:</b><br>
                    - 관세: 과세가격(CIF) × 20% (주류 관세율)<br>
                    - 주세: (과세가격 + 관세) × 72%<br>
                    - 교육세: 주세 × 30%<br>
                    - 부가가세: (과세가격 + 관세 + 주세 + 교육세) × 10%
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with tax_col2:
            # 세금 연산 시작
            cif_usd = product_price_usd + shipping_usd
            cif_krw = cif_usd * exchange_rate
            
            # 주류 세금 계산
            customs_tax = cif_krw * 0.20  # 관세 20%
            liquor_tax = (cif_krw + customs_tax) * 0.72  # 주세 72%
            education_tax = liquor_tax * 0.30  # 교육세 30%
            vat = (cif_krw + customs_tax + liquor_tax + education_tax) * 0.10  # 부가세 10%
            
            total_tax = customs_tax + liquor_tax + education_tax + vat
            final_price = cif_krw + total_tax
            
            # 주세 부과 전 실구매 상품가
            pure_goods_krw = product_price_usd * exchange_rate
            
            st.markdown("##### 📊 납부 세금 요약 명세서")
            st.markdown(
                f"""
                <div style="background-color:#1e1814; padding:20px; border-radius:10px; border:1px solid #4a382c;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:1.15rem; font-weight:bold; border-bottom:1px solid #3d2f25; padding-bottom:8px;">
                        <span style="color:#dfba6b;">최종 예상 총 비용</span>
                        <span style="color:#dfba6b;">{int(final_price):,}원</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.88rem;">
                        <span style="color:#a89984;">순수 물품대금 ({product_price_usd:.1f}$)</span>
                        <span>{int(pure_goods_krw):,}원</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.88rem;">
                        <span style="color:#a89984;">배송 비용 ({shipping_usd:.1f}$)</span>
                        <span>{int(shipping_usd * exchange_rate):,}원</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:0.88rem; border-bottom:1px solid #3d2f25; padding-bottom:8px;">
                        <span style="color:#a89984;">과세 기준액 (CIF)</span>
                        <span>{int(cif_krw):,}원</span>
                    </div>
                    
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.88rem; color:#ebd9c2;">
                        <span>1. 관세 (20%)</span>
                        <span>{int(customs_tax):,}원</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.88rem; color:#ebd9c2;">
                        <span>2. 주세 (72%)</span>
                        <span>{int(liquor_tax):,}원</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.88rem; color:#ebd9c2;">
                        <span>3. 교육세 (30%)</span>
                        <span>{int(education_tax):,}원</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:0.88rem; color:#ebd9c2; border-bottom:1px solid #3d2f25; padding-bottom:8px;">
                        <span>4. 부가세 (10%)</span>
                        <span>{int(vat):,}원</span>
                    </div>
                    
                    <div style="display:flex; justify-content:space-between; margin-top:10px; font-weight:bold; font-size:1.05rem; color:#e57373;">
                        <span>총 예상 세금 합계</span>
                        <span>{int(total_tax):,}원</span>
                    </div>
                    <p style="font-size:0.75rem; color:#a0907a; margin-top:15px; margin-bottom:0; text-align:center; font-style:italic;">
                        * 세율 과세 비율: 과세가격 대비 세금 비중은 약 <b>{round((total_tax / cif_krw) * 100, 1)}%</b>입니다 (주류 직구 시 관세폭탄의 주 요인).
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
    # 🧪 바이알(Vial) 분할 소분단가 계산기
    with calc_tab2:
        st.markdown("##### 🧪 바이알(Vial) 소분 몫당 원가 계산기")
        st.markdown("<p style='font-size:0.8rem; color:#a0907a;'>동호회나 모임에서 위스키 1병을 여러 개의 바이알 공병에 나누어 시음할 때, 공병값 및 재료비를 감안한 공정한 분할 단가를 구합니다.</p>", unsafe_allow_html=True)
        
        v_col1, v_col2 = st.columns([1, 1.2])
        
        with v_col1:
            bottle_cost = st.number_input("위스키 한 병 구매 원가 (원)", min_value=0, value=150000, step=5000)
            total_vol = st.number_input("위스키 병 총 용량 (ml)", min_value=10, max_value=5000, value=700, step=50)
            vial_vol = st.number_input("소분할 바이알 1개 용량 (ml)", min_value=5, max_value=500, value=30, step=5)
            vial_unit_cost = st.number_input("바이알 공병 + 라벨 스티커 1개당 단가 (원)", min_value=0, value=1500, step=100)
            etc_cost = st.number_input("기타 부대 비용 (택배 포장백, 파라필름 등 총액, 원)", min_value=0, value=3000, step=500)
            
        with v_col2:
            # 연산
            max_vials = total_vol // vial_vol
            pure_liquid_cost = (vial_vol / total_vol) * bottle_cost
            total_vials_to_make = max_vials
            
            # 기타 비용을 바이알 개수로 분배
            etc_cost_per_vial = etc_cost / total_vials_to_make if total_vials_to_make > 0 else 0
            final_vial_cost = pure_liquid_cost + vial_unit_cost + etc_cost_per_vial
            
            st.markdown("##### 📋 소분을 위한 몫 계산 결과")
            st.markdown(
                f"""
                <div style="background-color:#1e1814; padding:20px; border-radius:10px; border:1px solid #4a382c;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:1.15rem; font-weight:bold; border-bottom:1px solid #3d2f25; padding-bottom:8px;">
                        <span style="color:#dfba6b;">바이알 1개당 권장 정가</span>
                        <span style="color:#dfba6b;">{int(final_vial_cost):,}원</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.88rem;">
                        <span style="color:#a89984;">총 제작 가능한 바이알 수</span>
                        <span>{int(max_vials)}개</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.88rem;">
                        <span style="color:#a89984;">순수 주류 원액 비용 ({vial_vol}ml)</span>
                        <span>{int(pure_liquid_cost):,}원</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.88rem;">
                        <span style="color:#a89984;">바이알 부자재 비용 (공병 + 스티커)</span>
                        <span>{int(vial_unit_cost):,}원</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:0.88rem; border-bottom:1px solid #3d2f25; padding-bottom:8px;">
                        <span style="color:#a89984;">1개당 분배된 기타 공통비용</span>
                        <span>{int(etc_cost_per_vial):,}원</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-weight:bold; font-size:1.05rem; color:#ebd9c2;">
                        <span>모임 총 소요 예산액</span>
                        <span>{int(bottle_cost + (vial_unit_cost * max_vials) + etc_cost):,}원</span>
                    </div>
                    <p style="font-size:0.75rem; color:#a0907a; margin-top:15px; margin-bottom:0; text-align:center; font-style:italic;">
                        * 700ml 1병 기준, {vial_vol}ml씩 완벽하게 소분할 시 최대 <b>{int(max_vials)}명</b>이 함께 시음할 수 있는 분량입니다.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
