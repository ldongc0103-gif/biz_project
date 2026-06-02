# -*- coding: utf-8 -*-
"""
위스키 가이드 프리미엄 스타일 모듈
이 모듈은 Streamlit 애플리케이션의 기본 스타일을 변경하여 고풍스러운 위스키 바 느낌의 
다크 골드/앰버 테마를 구현하기 위해 Custom CSS 코드를 포함합니다.
"""

import streamlit as st

def apply_premium_styles():
    """Streamlit 앱 전체에 고유한 다크 프리미엄 CSS 테마를 주입합니다."""
    
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        
        <style>
        /* 폰트 및 배경 설정 */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0d0b0a;
            color: #f5f2eb;
            font-family: 'Inter', sans-serif;
        }
        
        /* 헤더 스타일링 */
        h1, h2, h3 {
            font-family: 'Cinzel', serif;
            color: #dfba6b !important;
            font-weight: 700;
        }
        
        /* 메인 배너 그라데이션 */
        .premium-banner {
            background: linear-gradient(135deg, #1f1813 0%, #120c08 100%);
            border: 1px solid #3d2f25;
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }
        
        .premium-banner::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #b8860b, #e6c280, #b8860b);
        }
        
        .premium-title {
            font-family: 'Cinzel', serif;
            font-size: 2.8rem;
            font-weight: 800;
            color: #dfba6b;
            letter-spacing: 2px;
            margin: 0;
            text-shadow: 0 0 10px rgba(223, 186, 107, 0.3);
        }
        
        .premium-subtitle {
            font-size: 1.1rem;
            color: #c7b9a5;
            margin-top: 10px;
            font-weight: 300;
            letter-spacing: 1px;
        }
        
        /* Glassmorphism 카드 컨테이너 */
        .whisky-card {
            background: rgba(26, 20, 16, 0.6);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(184, 134, 11, 0.15);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        
        .whisky-card:hover {
            border-color: rgba(223, 186, 107, 0.5);
            transform: translateY(-5px);
            box-shadow: 0 8px 30px rgba(184, 134, 11, 0.15);
        }
        
        /* 뱃지 태그 */
        .category-badge {
            background-color: #2b1f15;
            color: #dfba6b;
            border: 1px solid #b8860b;
            border-radius: 20px;
            padding: 3px 12px;
            font-size: 0.8rem;
            font-weight: 500;
            display: inline-block;
            margin-bottom: 10px;
        }
        
        .origin-badge {
            background-color: #171c19;
            color: #8bbfa3;
            border: 1px solid #4a755d;
            border-radius: 20px;
            padding: 3px 12px;
            font-size: 0.8rem;
            font-weight: 500;
            display: inline-block;
            margin-bottom: 10px;
            margin-left: 5px;
        }
        
        /* 테이스팅 노트 박스 */
        .tasting-note-box {
            background-color: #14110e;
            border-left: 3px solid #dfba6b;
            padding: 12px;
            margin-top: 10px;
            border-radius: 0 8px 8px 0;
            font-size: 0.9rem;
        }
        
        .note-title {
            font-weight: 600;
            color: #dfba6b;
            margin-bottom: 4px;
        }
        
        /* 사이드바 커스텀 */
        section[data-testid="stSidebar"] {
            background-color: #120e0c !important;
            border-right: 1px solid #281f18;
        }
        
        /* 위젯 커스텀 (스트림릿 슬라이더, 셀렉트박스 등) */
        .stSelectbox, .stMultiSelect, .stSlider {
            background-color: transparent !important;
        }
        
        div[data-baseweb="select"] {
            background-color: #1a1511 !important;
            border-color: #3d2f25 !important;
        }
        
        div[role="listbox"] {
            background-color: #1a1511 !important;
        }
        
        /* 버튼 커스텀 */
        .stButton>button {
            background: linear-gradient(135deg, #b8860b 0%, #8b6508 100%) !important;
            color: #ffffff !important;
            border: 1px solid #e6c280 !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 15px rgba(184, 134, 11, 0.2) !important;
        }
        
        .stButton>button:hover {
            background: linear-gradient(135deg, #dfba6b 0%, #b8860b 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(184, 134, 11, 0.4) !important;
        }
        
        /* 탭 스타일링 */
        button[data-baseweb="tab"] {
            font-family: 'Cinzel', serif !important;
            font-size: 1rem !important;
            letter-spacing: 1px !important;
            color: #a79a85 !important;
            background-color: transparent !important;
            padding: 12px 20px !important;
            border-bottom: 2px solid transparent !important;
            transition: all 0.3s !important;
        }
        
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #dfba6b !important;
            border-bottom-color: #dfba6b !important;
            font-weight: bold !important;
        }
        
        /* 메트릭 스타일 */
        div[data-testid="stMetric"] {
            background-color: #1a1410;
            border: 1px solid #382b20;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        div[data-testid="stMetricLabel"] {
            color: #a0907a !important;
        }
        div[data-testid="stMetricValue"] {
            color: #dfba6b !important;
        }
        
        /* 구분선 */
        hr {
            border-color: #2b1f15 !important;
            margin: 30px 0 !important;
        }
        
        /* 테이블/판다스 데이터프레임 스타일 */
        div[data-testid="stDataFrame"] {
            background-color: #1a1410 !important;
            border: 1px solid #2d2319 !important;
            border-radius: 8px;
        }
        
        /* 시각화 차트 프레임 스타일 */
        .chart-container {
            background-color: #14100c;
            border: 1px solid #281f18;
            border-radius: 12px;
            padding: 15px;
            margin-top: 15px;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

def premium_card_html(whisky):
    """위스키 정보를 담은 HTML 카드 코드를 생성하여 반환합니다."""
    # 가장 대중적인 대형마트/스마트오더 가격 포맷팅
    price_fmt = f"{whisky['current_prices']['대형마트/스마트오더']:,}"
    
    html = f"""
    <div class="whisky-card">
        <div style="width: 100%; height: 180px; overflow: hidden; border-radius: 8px; margin-bottom: 15px; border: 1px solid rgba(184, 134, 11, 0.15);">
            <img src="{whisky['image_url']}" style="width: 100%; height: 100%; object-fit: cover;" alt="{whisky['name_ko']}">
        </div>
        <span class="category-badge">{whisky['category']}</span>
        <span class="origin-badge">{whisky['origin']}</span>
        <h3 style="margin-top:5px; margin-bottom:2px; font-size:1.2rem; color:#dfba6b;">{whisky['name_ko']}</h3>
        <p style="color:#a89984; font-size:0.8rem; margin-top:0; font-style:italic; margin-bottom:12px;">{whisky['name_en']} ({whisky['abv']}% / {whisky['age']}Y)</p>
        <p style="font-size:0.85rem; color:#ebd9c2; line-height:1.5; height: 75px; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;">{whisky['description']}</p>
        
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:15px; padding-top:15px; border-top:1px solid #2b1f15;">
            <span style="font-size:0.8rem; color:#8e8270;">마트/스마트오더 평균가</span>
            <span style="font-size:1.15rem; font-weight:700; color:#dfba6b;">{price_fmt}원</span>
        </div>
    </div>
    """
    return html
