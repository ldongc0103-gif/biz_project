# -*- coding: utf-8 -*-
"""
위스키 프리미엄 데이터베이스 모듈
이 모듈은 웹 앱에서 사용할 유명 위스키 30종의 맛 프로필, 카테고리, 
판매처별 가격 비교 정보 및 12개월간의 가격 트렌드 데이터를 저장하고 제공합니다.
"""

import pandas as pd
import numpy as np

# 위스키 원본 데이터셋 정의
WHISKY_DATA = [
    # --- 싱글 몰트 스카치 위스키 (Single Malt Scotch) ---
    {
        "id": "macallan_12_sherry",
        "name_ko": "맥캘란 12년 셰리오크",
        "name_en": "Macallan 12 Year Old Sherry Oak",
        "category": "싱글몰트",
        "origin": "스코틀랜드 (스페이사이드)",
        "abv": 40.0,
        "age": "12",
        "image_url": "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?auto=format&fit=crop&q=80&w=600",
        "description": "싱글몰트 위스키의 명가 맥캘란의 대표 라인업으로, 스페인 헤레스(Jerez)의 셰리 오크통에서 숙성되어 풍부하고 깊은 과일 향과 나무 향을 선사하는 정통 셰리 위스키의 기준입니다.",
        "tasting_notes": {
            "Nose": "말린 과일, 달콤한 바닐라, 생강, 시나몬의 알싸한 향",
            "Palate": "부드럽고 묵직한 단맛, 셰리 와인의 깊은 풍미, 오크와 스파이스",
            "Finish": "길고 따뜻한 셰리 잔향, 말린 오렌지와 약간의 훈연향"
        },
        "taste_profile": {
            "단맛(Sweetness)": 8,
            "피트감(Peat)": 1,
            "셰리/과일(Sherry)": 9,
            "오크/나무(Oak)": 7,
            "바디감(Body)": 8
        },
        "current_prices": {
            "대형마트/스마트오더": 139000,
            "남대문/주류상가": 120000,
            "제주/해외면세점": 105000,
            "해외직구(세금포함)": 178000
        },
        # 지난 12개월 평균 소매가 추이
        "price_history": [148000, 145000, 143000, 141000, 139000, 137000, 135000, 135000, 136000, 137000, 138000, 139000]
    },
    {
        "id": "balvenie_12_doublewood",
        "name_ko": "발베니 12년 더블우드",
        "name_en": "Balvenie 12 Year Old DoubleWood",
        "category": "싱글몰트",
        "origin": "스코틀랜드 (스페이사이드)",
        "abv": 40.0,
        "age": "12",
        "image_url": "https://images.unsplash.com/photo-1569529465841-dfedd87500f7?auto=format&fit=crop&q=80&w=600",
        "description": "아메리칸 버번 오크통과 유러피안 셰리 오크통 두 가지에서 숙성시키는 '우드 피니시' 기법의 선구자적 위스키로, 부드러운 꿀맛과 바닐라 향이 일품인 부드러운 대중적 몰트입니다.",
        "tasting_notes": {
            "Nose": "부드러운 꿀, 화사한 과일 향, 달콤한 셰리의 복합적인 조화",
            "Palate": "부드럽고 감미로운 꿀, 견과류의 고소함, 은은한 시나몬 스파이스",
            "Finish": "길고 부드러우며 마음을 편안하게 해주는 따뜻한 오크 향"
        },
        "taste_profile": {
            "단맛(Sweetness)": 8,
            "피트감(Peat)": 1,
            "셰리/과일(Sherry)": 7,
            "오크/나무(Oak)": 6,
            "바디감(Body)": 6
        },
        "current_prices": {
            "대형마트/스마트오더": 115000,
            "남대문/주류상가": 98000,
            "제주/해외면세점": 89000,
            "해외직구(세금포함)": 155000
        },
        "price_history": [135000, 130000, 128000, 125000, 120000, 118000, 115000, 113000, 112000, 114000, 115000, 115000]
    },
    {
        "id": "glenfiddich_15",
        "name_ko": "글렌피딕 15년",
        "name_en": "Glenfiddich 15 Year Old Solera",
        "category": "싱글몰트",
        "origin": "스코틀랜드 (스페이사이드)",
        "abv": 40.0,
        "age": "15",
        "image_url": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&q=80&w=600",
        "description": "스페인의 셰리 양조 방식에서 영감을 받은 '솔레라 바트(Solera Vat)' 기법을 도입하여 숙성 연수 대비 훨씬 깊은 밸런스와 달콤한 꿀, 무화과 풍미를 구현해낸 균형 잡힌 위스키입니다.",
        "tasting_notes": {
            "Nose": "붉은 사과, 꿀, 풍부한 헤더 꽃 향과 셰리의 복잡성",
            "Palate": "부드럽고 실키한 질감, 꿀, 마지팬, 생강, 건포도의 다채로운 풍미",
            "Finish": "부드럽고 깊은 피니시, 기분 좋은 단맛과 오크의 여운"
        },
        "taste_profile": {
            "단맛(Sweetness)": 7,
            "피트감(Peat)": 1,
            "셰리/과일(Sherry)": 8,
            "오크/나무(Oak)": 7,
            "바디감(Body)": 7
        },
        "current_prices": {
            "대형마트/스마트오더": 145000,
            "남대문/주류상가": 122000,
            "제주/해외면세점": 105000,
            "해외직구(세금포함)": 182000
        },
        "price_history": [152000, 150000, 148000, 147000, 145000, 142000, 140000, 140000, 142000, 143000, 145000, 145000]
    },
    {
        "id": "glendronach_12",
        "name_ko": "글렌드로낙 12년",
        "name_en": "Glendronach 12 Year Old Original",
        "category": "싱글몰트",
        "origin": "스코틀랜드 (하일랜드)",
        "abv": 43.0,
        "age": "12",
        "image_url": "https://images.unsplash.com/photo-1508253730747-e83d57821c90?auto=format&fit=crop&q=80&w=600",
        "description": "스페인의 최고급 올로로소(Oloroso)와 페드로 히메네스(Pedro Ximenez) 셰리 오크통에서 풀타임 숙성되어 강렬한 건자두, 초콜릿, 견과류 향을 선사하는 소위 '셰리 괴물'의 대표작입니다.",
        "tasting_notes": {
            "Nose": "진한 달콤함, 크리미한 바닐라, 생강, 은은한 가을 낙엽 향",
            "Palate": "초콜릿, 잘 익은 건포도, 자두, 풍부하고 크리미한 마우스필",
            "Finish": "초콜릿과 말린 과일의 단 여운이 입안 전체를 감쌈"
        },
        "taste_profile": {
            "단맛(Sweetness)": 9,
            "피트감(Peat)": 1,
            "셰리/과일(Sherry)": 10,
            "오크/나무(Oak)": 6,
            "바디감(Body)": 8
        },
        "current_prices": {
            "대형마트/스마트오더": 118000,
            "남대문/주류상가": 95000,
            "제주/해외면세점": 85000,
            "해외직구(세금포함)": 160000
        },
        "price_history": [128000, 125000, 122000, 120000, 118000, 115000, 113000, 114000, 115000, 116000, 117000, 118000]
    },
    {
        "id": "glenmorangie_original",
        "name_ko": "글렌모렌지 오리지널 10년",
        "name_en": "Glenmorangie The Original 10 Year Old",
        "category": "싱글몰트",
        "origin": "스코틀랜드 (하일랜드)",
        "abv": 40.0,
        "age": "10",
        "image_url": "https://images.unsplash.com/photo-1618260700578-2a6288efd194?auto=format&fit=crop&q=80&w=600",
        "description": "기린만큼 목이 긴 스코틀랜드에서 가장 높은 증류기를 사용하여 매우 가볍고 순수하며, 감귤류와 복숭아 등 다채로운 과일 향과 화사함을 지닌 여성적인 매력의 싱글몰트입니다.",
        "tasting_notes": {
            "Nose": "감귤, 잘 익은 복숭아, 꽃향기, 달콤한 바닐라",
            "Palate": "꽃향기를 머금은 꿀, 부드러운 오렌지 에센스, 크리미한 바닐라 타르트",
            "Finish": "깔끔하고 상쾌하며 은은한 복숭아와 몰트의 깔끔함"
        },
        "taste_profile": {
            "단맛(Sweetness)": 7,
            "피트감(Peat)": 1,
            "셰리/과일(Sherry)": 6,
            "오크/나무(Oak)": 4,
            "바디감(Body)": 4
        },
        "current_prices": {
            "대형마트/스마트오더": 89000,
            "남대문/주류상가": 72000,
            "제주/해외면세점": 65000,
            "해외직구(세금포함)": 132000
        },
        "price_history": [98000, 95000, 92000, 90000, 89000, 85000, 83000, 84000, 86000, 87000, 88000, 89000]
    },
    {
        "id": "lagavulin_16",
        "name_ko": "라가불린 16년",
        "name_en": "Lagavulin 16 Year Old",
        "category": "싱글몰트",
        "origin": "스코틀랜드 (아일라)",
        "abv": 43.0,
        "age": "16",
        "image_url": "https://images.unsplash.com/photo-1582819509237-d5b75f20ab7a?auto=format&fit=crop&q=80&w=600",
        "description": "아일라 섬의 피트 위스키 중 가장 우아하고 클래식하다고 평가받는 16년 숙성 위스키입니다. 강력한 약용 향, 이탄 향과 함께 셰리 오크통에서 오는 깊고 달콤한 과일 향이 환상적인 대조를 이룹니다.",
        "tasting_notes": {
            "Nose": "매우 강렬한 피트 연기, 바닷바람의 짠맛, 달콤한 셰리와 무화과",
            "Palate": "두꺼운 연기, 폭발하는 스파이스, 맥아의 단맛, 드라이한 오크",
            "Finish": "엄청나게 길고 깊은 여운, 연기와 피트, 소금기 서린 무화과"
        },
        "taste_profile": {
            "단맛(Sweetness)": 6,
            "피트감(Peat)": 10,
            "셰리/과일(Sherry)": 7,
            "오크/나무(Oak)": 8,
            "바디감(Body)": 9
        },
        "current_prices": {
            "대형마트/스마트오더": 158000,
            "남대문/주류상가": 139000,
            "제주/해외면세점": 118000,
            "해외직구(세금포함)": 210000
        },
        "price_history": [185000, 180000, 175000, 168000, 162000, 158000, 150000, 152000, 154000, 155000, 156000, 158000]
    },
    {
        "id": "ardbeg_10",
        "name_ko": "아드벡 10년",
        "name_en": "Ardbeg 10 Year Old",
        "category": "싱글몰트",
        "origin": "스코틀랜드 (아일라)",
        "abv": 46.0,
        "age": "10",
        "image_url": "https://images.unsplash.com/photo-1508253730747-e83d57821c90?auto=format&fit=crop&q=80&w=600",
        "description": "아일라 피트 매니아들의 지지를 받는 가장 자극적이고 원초적인 위스키입니다. 여과 과정을 거치지 않는 Non-Chill Filtered 방식으로 병입되어 레몬, 라임의 시트러스함과 극대화된 스모키 피트 향이 특징입니다.",
        "tasting_notes": {
            "Nose": "폭발적인 이탄 연기, 레몬 필, 시트러스, 알싸한 흑후추",
            "Palate": "강한 피트, 크레오소트, 레몬 타르트, 소금기, 바닐라 토피의 갑작스러운 단맛",
            "Finish": "길고 스모키하며, 구운 보리, 훈제 연기와 타르의 끈질긴 피니시"
        },
        "taste_profile": {
            "단맛(Sweetness)": 4,
            "피트감(Peat)": 10,
            "셰리/과일(Sherry)": 2,
            "오크/나무(Oak)": 6,
            "바디감(Body)": 8
        },
        "current_prices": {
            "대형마트/스마트오더": 105000,
            "남대문/주류상가": 88000,
            "제주/해외면세점": 78000,
            "해외직구(세금포함)": 148000
        },
        "price_history": [115000, 112000, 110000, 108000, 105000, 103000, 100000, 101000, 103000, 104000, 104000, 105000]
    },
    {
        "id": "talisker_10",
        "name_ko": "탈리스커 10년",
        "name_en": "Talisker 10 Year Old",
        "category": "싱글몰트",
        "origin": "스코틀랜드 (스카이섬)",
        "abv": 45.8,
        "age": "10",
        "image_url": "https://images.unsplash.com/photo-1628435759132-72c05ad625c2?auto=format&fit=crop&q=80&w=600",
        "description": "스카이(Skye) 섬의 거친 바다 기후 속에서 태어나 '바다의 위스키'로 불립니다. 짭조름한 소금 바닷바람 향과 뒤이어 후추를 한가득 뿌린 듯한 알싸한 스파이시함이 대조적인 인상을 줍니다.",
        "tasting_notes": {
            "Nose": "피트 연기, 짭조름한 소금기, 신선한 굴, 시트러스한 오렌지 껍질",
            "Palate": "말린 과일의 은은한 단맛 뒤에 찾아오는 폭발적인 통후추와 스모크",
            "Finish": "엄청나게 뜨겁고 스파이시한 여운, 보리 맥아의 구수함과 기분 좋은 타르 향"
        },
        "taste_profile": {
            "단맛(Sweetness)": 5,
            "피트감(Peat)": 8,
            "셰리/과일(Sherry)": 4,
            "오크/나무(Oak)": 6,
            "바디감(Body)": 7
        },
        "current_prices": {
            "대형마트/스마트오더": 75000,
            "남대문/주류상가": 62000,
            "제주/해외면세점": 55000,
            "해외직구(세금포함)": 115000
        },
        "price_history": [85000, 82000, 80000, 78000, 75000, 73000, 70000, 71000, 73000, 74000, 74000, 75000]
    },
    {
        "id": "laphroaig_10",
        "name_ko": "라프로익 10년",
        "name_en": "Laphroaig 10 Year Old",
        "category": "싱글몰트",
        "origin": "스코틀랜드 (아일라)",
        "abv": 40.0,
        "age": "10",
        "image_url": "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?auto=format&fit=crop&q=80&w=600",
        "description": "찰스 3세 국왕의 로열 워런트를 획득한 왕실 공식 위스키로, '좋아하거나 혹은 싫어하거나(Love it or Hate it)'로 유명한 강한 소독약(정로환) 향이 전매특허인 개성 만점 싱글몰트입니다.",
        "tasting_notes": {
            "Nose": "매우 매캐하고 소독약 같은 약용 피트 향, 해조류, 짠 소금 냄새",
            "Palate": "강한 이탄 연기, 구운 견과류, 바닐라 에센스의 은은한 단맛과 알싸함",
            "Finish": "소독제 연기, 해초, 매우 드라이하고 깔끔하며 잊지 못할 짠 여운"
        },
        "taste_profile": {
            "단맛(Sweetness)": 5,
            "피트감(Peat)": 10,
            "셰리/과일(Sherry)": 3,
            "오크/나무(Oak)": 5,
            "바디감(Body)": 8
        },
        "current_prices": {
            "대형마트/스마트오더": 99000,
            "남대문/주류상가": 82000,
            "제주/해외면세점": 72000,
            "해외직구(세금포함)": 139000
        },
        "price_history": [108000, 105000, 102000, 100000, 99000, 95000, 92000, 93000, 95000, 96000, 97000, 99000]
    },
    {
        "id": "glenallachie_12",
        "name_ko": "글렌알라키 12년",
        "name_en": "GlenAllachie 12 Year Old",
        "category": "싱글몰트",
        "origin": "스코틀랜드 (스페이사이드)",
        "abv": 46.0,
        "age": "12",
        "image_url": "https://images.unsplash.com/photo-1569529465841-dfedd87500f7?auto=format&fit=crop&q=80&w=600",
        "description": "위스키 업계의 살아있는 전설 빌리 워커(Billy Walker)가 인수한 후 전 세계적으로 초히트를 친 셰리 중심 싱글몰트입니다. 46도의 강한 도수와 깊은 무화과 및 시나몬 터치로 두터운 매니아층을 형성하고 있습니다.",
        "tasting_notes": {
            "Nose": "풍부한 꿀, 바나나 필, 자두, 시나몬의 알싸한 향",
            "Palate": "꿀, 헤더, 다크 초콜릿, 잘 익은 건포도와 톡 쏘는 생강 스파이스",
            "Finish": "길고 부드러우며 다크 초콜릿과 모카의 진한 단맛"
        },
        "taste_profile": {
            "단맛(Sweetness)": 8,
            "피트감(Peat)": 1,
            "셰리/과일(Sherry)": 9,
            "오크/나무(Oak)": 6,
            "바디감(Body)": 7
        },
        "current_prices": {
            "대형마트/스마트오더": 112000,
            "남대문/주류상가": 93000,
            "제주/해외면세점": 82000,
            "해외직구(세금포함)": 158000
        },
        "price_history": [128000, 123000, 120000, 116000, 112000, 110000, 108000, 107000, 109000, 110000, 111000, 112000]
    },

    # --- 블렌디드 스카치 위스키 (Blended Scotch) ---
    {
        "id": "johnnie_black",
        "name_ko": "조니워커 블랙라벨",
        "name_en": "Johnnie Walker Black Label",
        "category": "블렌디드",
        "origin": "스코틀랜드",
        "abv": 40.0,
        "age": "12",
        "image_url": "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?auto=format&fit=crop&q=80&w=600",
        "description": "블렌디드 위스키의 정석이자 교과서입니다. 12년 이상 숙성된 40여 가지 몰트와 그레인 위스키를 절묘하게 믹싱하여 달콤함, 풍부한 과일 향, 특유의 바닐라 풍미와 드라이한 스모키함이 완벽하게 균형을 이룹니다.",
        "tasting_notes": {
            "Nose": "달콤한 건과일 향, 오렌지 시트러스, 스모키한 피트 아로마",
            "Palate": "달콤하고 크리미한 바닐라, 신선한 보리, 잘 구워진 나무, 은은한 스파이시",
            "Finish": "매우 매끄럽고 부드러운 스모키 피니시와 기분 좋은 몰트 잔향"
        },
        "taste_profile": {
            "단맛(Sweetness)": 6,
            "피트감(Peat)": 5,
            "셰리/과일(Sherry)": 5,
            "오크/나무(Oak)": 5,
            "바디감(Body)": 6
        },
        "current_prices": {
            "대형마트/스마트오더": 46000,
            "남대문/주류상가": 38000,
            "제주/해외면세점": 33000,
            "해외직구(세금포함)": 78000
        },
        "price_history": [49000, 48000, 47000, 47000, 46000, 45000, 45000, 45000, 45000, 46000, 46000, 46000]
    },
    {
        "id": "johnnie_blue",
        "name_ko": "조니워커 블루라벨",
        "name_en": "Johnnie Walker Blue Label",
        "category": "블렌디드",
        "origin": "스코틀랜드",
        "abv": 40.0,
        "age": "NAS",
        "image_url": "https://images.unsplash.com/photo-1569529465841-dfedd87500f7?auto=format&fit=crop&q=80&w=600",
        "description": "조니워커 가문의 마스터 블렌더가 10,000개의 오크통 중 단 하나씩만 골라낸 극도로 희귀한 원액들로 만든 하이엔드 럭셔리 위스키입니다. 벨벳처럼 부드러운 목 넘김과 함께 스모키, 바닐라, 과일향이 물 흐르듯 번집니다.",
        "tasting_notes": {
            "Nose": "헤이즐넛, 꿀, 장미 향기와 달콤한 셰리 오렌지 아로마",
            "Palate": "부드럽고 묵직한 마우스필, 백단향, 초콜릿, 달콤한 꿀과 서서히 번지는 연기",
            "Finish": "놀라울 정도로 길고 매끈한 여운, 부드러운 스모키 피트와 향신료의 축제"
        },
        "taste_profile": {
            "단맛(Sweetness)": 8,
            "피트감(Peat)": 4,
            "셰리/과일(Sherry)": 8,
            "오크/나무(Oak)": 7,
            "바디감(Body)": 9
        },
        "current_prices": {
            "대형마트/스마트오더": 310000,
            "남대문/주류상가": 255000,
            "제주/해외면세점": 218000,
            "해외직구(세금포함)": 395000
        },
        "price_history": [330000, 325000, 320000, 315000, 310000, 305000, 298000, 300000, 302000, 305000, 308000, 310000]
    },
    {
        "id": "ballantines_17",
        "name_ko": "발렌타인 17년",
        "name_en": "Ballantine's 17 Year Old",
        "category": "블렌디드",
        "origin": "스코틀랜드",
        "abv": 40.0,
        "age": "17",
        "image_url": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&q=80&w=600",
        "description": "국내에서 압도적인 인지도를 누리고 있는 '비즈니스 위스키'의 대명사입니다. 17년간 오크통 속에서 부드럽게 에이징되어 우아하고 화사한 향과 은은한 바닐라, 감미로운 목 넘김을 완성하였습니다.",
        "tasting_notes": {
            "Nose": "은은한 바닐라, 오크 향, 잘 익은 배와 화사한 꿀 향기",
            "Palate": "부드럽고 깊은 벨벳 풍미, 꿀의 달콤함, 약간의 감초와 오크 스파이스",
            "Finish": "바닐라와 연한 스모크 향이 감미롭고 조화롭게 마무리됨"
        },
        "taste_profile": {
            "단맛(Sweetness)": 7,
            "피트감(Peat)": 2,
            "셰리/과일(Sherry)": 6,
            "오크/나무(Oak)": 6,
            "바디감(Body)": 7
        },
        "current_prices": {
            "대형마트/스마트오더": 139000,
            "남대문/주류상가": 105000,
            "제주/해외면세점": 93000,
            "해외직구(세금포함)": 185000
        },
        "price_history": [152000, 148000, 145000, 142000, 139000, 136000, 133000, 134000, 135000, 136000, 138000, 139000]
    },
    {
        "id": "ballantines_21",
        "name_ko": "발렌타인 21년",
        "name_en": "Ballantine's 21 Year Old",
        "category": "블렌디드",
        "origin": "스코틀랜드",
        "abv": 40.0,
        "age": "21",
        "image_url": "https://images.unsplash.com/photo-1508253730747-e83d57821c90?auto=format&fit=crop&q=80&w=600",
        "description": "우아함과 고품격의 극치를 지닌 스카치 위스키입니다. 바닐라 향에 셰리 오크통에서 유래된 진한 건과일 맛과 향긋한 스파이시함이 깊숙이 조화를 이루어 대단히 고급스러운 맛을 완성했습니다.",
        "tasting_notes": {
            "Nose": "진하고 우아한 과일 아로마, 바닐라 타르트, 꽃향기와 시나몬",
            "Palate": "부드럽고 묵직한 단맛, 건포도, 아몬드의 고소함, 매끄러운 바닐라 시럽",
            "Finish": "매우 길고 중후한 피니시, 가벼운 셰리 잔향과 훈연 오크의 정제된 마무리"
        },
        "taste_profile": {
            "단맛(Sweetness)": 8,
            "피트감(Peat)": 2,
            "셰리/과일(Sherry)": 8,
            "오크/나무(Oak)": 7,
            "바디감(Body)": 8
        },
        "current_prices": {
            "대형마트/스마트오더": 220000,
            "남대문/주류상가": 178000,
            "제주/해외면세점": 155000,
            "해외직구(세금포함)": 298000
        },
        "price_history": [245000, 240000, 235000, 230000, 220000, 215000, 210000, 211000, 214000, 216000, 218000, 220000]
    },
    {
        "id": "royal_salute_21",
        "name_ko": "로얄살루트 21년 시그니처",
        "name_en": "Royal Salute 21 Year Old Signature",
        "category": "블렌디드",
        "origin": "스코틀랜드",
        "abv": 40.0,
        "age": "21",
        "image_url": "https://images.unsplash.com/photo-1618260700578-2a6288efd194?auto=format&fit=crop&q=80&w=600",
        "description": "1953년 엘리자베스 2세 여왕의 대관식에 바치기 위해 21발의 예포(Royal Salute)에서 유래하여 제작된 유서 깊은 왕실 위스키입니다. 도자기 병에 담겨 있으며, 최고급 스페이사이드 원액들의 농밀한 시트러스와 복숭아 잼 향이 일품입니다.",
        "tasting_notes": {
            "Nose": "잘 익은 배, 멜론, 향긋한 가을 꽃, 풍부한 바닐라와 달콤한 오렌지 마멀레이드",
            "Palate": "부드럽고 꽉 찬 단맛, 스파이시한 생각과 정향, 잘 익은 자두와 살구의 꿀물 같은 풍미",
            "Finish": "바닐라 꿀 향이 입속에 끝없이 맴돌며 따뜻하게 차오름"
        },
        "taste_profile": {
            "단맛(Sweetness)": 8,
            "피트감(Peat)": 2,
            "셰리/과일(Sherry)": 8,
            "오크/나무(Oak)": 6,
            "바디감(Body)": 8
        },
        "current_prices": {
            "대형마트/스마트오더": 235000,
            "남대문/주류상가": 182000,
            "제주/해외면세점": 160000,
            "해외직구(세금포함)": 315000
        },
        "price_history": [255000, 250000, 246000, 240000, 235000, 228000, 222000, 224000, 226000, 229000, 232000, 235000]
    },

    # --- 아메리칸 버번 위스키 (American Bourbon) ---
    {
        "id": "wild_turkey_101",
        "name_ko": "와일드 터키 101 8년",
        "name_en": "Wild Turkey 101 8 Year Old",
        "category": "버번",
        "origin": "미국 (켄터키)",
        "abv": 50.5,
        "age": "8",
        "image_url": "https://images.unsplash.com/photo-1628435759132-72c05ad625c2?auto=format&fit=crop&q=80&w=600",
        "description": "버번의 교과서이자 타격감 최강의 위스키입니다. 호밀(Rye) 함량이 높아 특유의 알싸함이 강하며, 50.5도(101 프루프)의 높은 알코올 도수에서 오는 압도적인 바닐라, 캐러멜, 그리고 강력한 가죽 및 오크 타격감을 자랑합니다.",
        "tasting_notes": {
            "Nose": "진한 캐러멜, 바닐라, 매콤한 시나몬과 그을린 강렬한 오크",
            "Palate": "높은 도수의 찌릿한 타격감, 메이플 시럽, 호밀 스파이시, 오렌지 시트러스",
            "Finish": "호밀 후추 향과 담배 잎, 그을린 가죽, 진한 초콜릿의 기분 좋은 쌉쌀함"
        },
        "taste_profile": {
            "단맛(Sweetness)": 8,
            "피트감(Peat)": 1,
            "셰리/과일(Sherry)": 3,
            "오크/나무(Oak)": 9,
            "바디감(Body)": 9
        },
        "current_prices": {
            "대형마트/스마트오더": 58000,
            "남대문/주류상가": 47000,
            "제주/해외면세점": 42000,
            "해외직구(세금포함)": 95000
        },
        "price_history": [62000, 60000, 59000, 59000, 58000, 56000, 55000, 55000, 56000, 57000, 58000, 58000]
    },
    {
        "id": "makers_mark",
        "name_ko": "메이커스 마크",
        "name_en": "Maker's Mark",
        "category": "버번",
        "origin": "미국 (켄터키)",
        "abv": 45.0,
        "age": "NAS",
        "image_url": "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?auto=format&fit=crop&q=80&w=600",
        "description": "빨간 밀봉 왁스 디자인으로 유명한 버번 위스키입니다. 일반적인 호밀(Rye) 대신 붉은 겨울밀(Winter Wheat)을 사용하여 찌르는 알싸함 대신 극강의 부드러움과 달콤한 빵, 캐러멜 향을 느낄 수 있는 대표 밀버번입니다.",
        "tasting_notes": {
            "Nose": "달콤한 밀 빵, 바닐라 에센스, 카카오, 아세톤 터치",
            "Palate": "부드럽고 기분 좋은 바닐라, 캐러멜, 은은한 견과류와 복숭아 잼",
            "Finish": "부드럽고 은은하게 끝맺는 나무 향과 달콤한 버터스카치"
        },
        "taste_profile": {
            "단맛(Sweetness)": 9,
            "피트감(Peat)": 1,
            "셰리/과일(Sherry)": 4,
            "오크/나무(Oak)": 6,
            "바디감(Body)": 7
        },
        "current_prices": {
            "대형마트/스마트오더": 59000,
            "남대문/주류상가": 48000,
            "제주/해외면세점": 43000,
            "해외직구(세금포함)": 98000
        },
        "price_history": [64000, 62000, 61000, 60000, 59000, 57000, 56000, 56000, 57000, 58000, 59000, 59000]
    },
    {
        "id": "woodford_reserve",
        "name_ko": "우드포드 리저브",
        "name_en": "Woodford Reserve",
        "category": "버번",
        "origin": "미국 (켄터키)",
        "abv": 43.2,
        "age": "NAS",
        "image_url": "https://images.unsplash.com/photo-1569529465841-dfedd87500f7?auto=format&fit=crop&q=80&w=600",
        "description": "전통 구리 단식 증류기로 3회 증류하여 석조 창고에서 천천히 숙성시킨 고급 버번입니다. 일반 버번 대비 아세톤 향이 현저히 적고, 부드러운 실크 질감에 바닐라, 견과류, 민트, 건과일 향까지 번지는 우아한 매력을 지니고 있습니다.",
        "tasting_notes": {
            "Nose": "다크 초콜릿, 오렌지 필, 건과일, 은은한 시나몬과 바닐라 왁스",
            "Palate": "부드럽고 달콤함, 에스프레소, 민트, 스파이시한 토피 사탕과 호두",
            "Finish": "매우 매끄럽고 잔잔하게 이어지는 크리미 오크 여운"
        },
        "taste_profile": {
            "단맛(Sweetness)": 8,
            "피트감(Peat)": 1,
            "셰리/과일(Sherry)": 6,
            "오크/나무(Oak)": 7,
            "바디감(Body)": 8
        },
        "current_prices": {
            "대형마트/스마트오더": 95000,
            "남대문/주류상가": 78000,
            "제주/해외면세점": 68000,
            "해외직구(세금포함)": 139000
        },
        "price_history": [105000, 102000, 99000, 97000, 95000, 92000, 89000, 90000, 92000, 93000, 94000, 95000]
    },
    {
        "id": "buffalo_trace",
        "name_ko": "버팔로 트레이스",
        "name_en": "Buffalo Trace",
        "category": "버번",
        "origin": "미국 (켄터키)",
        "abv": 40.0,
        "age": "NAS",
        "image_url": "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?auto=format&fit=crop&q=80&w=600",
        "description": "세계에서 가장 상을 많이 받은 증류소 중 하나인 버팔로 트레이스의 시그니처 버번입니다. 부담스럽지 않은 40도의 도수와 대중적으로 직관적인 캐러멜, 바닐라, 호밀 향이 균형적으로 잡혀 입문용 버번으로 극찬받습니다.",
        "tasting_notes": {
            "Nose": "달콤한 메이플 꿀, 캐러멜, 은은한 오렌지 오일과 정향",
            "Palate": "가볍고 부드러움, 호밀 스파이시의 톡 쏘는 맛, 갈색 설탕과 오크 향",
            "Finish": "깔끔하며, 바닐라 아이스크림과 옥수수의 은은한 단 여운"
        },
        "taste_profile": {
            "단맛(Sweetness)": 7,
            "피트감(Peat)": 1,
            "셰리/과일(Sherry)": 4,
            "오크/나무(Oak)": 6,
            "바디감(Body)": 6
        },
        "current_prices": {
            "대형마트/스마트오더": 49000,
            "남대문/주류상가": 39000,
            "제주/해외면세점": 34000,
            "해외직구(세금포함)": 82000
        },
        "price_history": [53000, 52000, 51000, 50000, 49000, 47000, 46000, 46000, 47000, 48000, 48000, 49000]
    },

    # --- 일본 / 기타 위스키 (Japanese, Irish & World) ---
    {
        "id": "yamazaki_12",
        "name_ko": "야마자키 12년",
        "name_en": "Yamazaki 12 Year Old",
        "category": "기타/일본",
        "origin": "일본 (오사카)",
        "abv": 43.0,
        "age": "12",
        "image_url": "https://images.unsplash.com/photo-1508253730747-e83d57821c90?auto=format&fit=crop&q=80&w=600",
        "description": "일본 최초의 증류소이자 전 세계 몰트 매니아들을 사로잡은 산토리 사의 시그니처 몰트 위스키입니다. 은은하고 오묘한 일본 참나무인 '미즈나라(Mizunara)' 오크통 원액이 블렌딩되어 절간의 향을 연상시키는 이색적인 향이 매력적입니다.",
        "tasting_notes": {
            "Nose": "복숭아, 파인애플, 미즈나라 참나무 향, 오리엔탈 스파이스",
            "Palate": "부드럽고 크리미함, 코코넛, 잘 익은 감귤, 잘 코팅된 크렘 브륄레",
            "Finish": "매우 깊고 조화로우며, 계피와 나무, 달콤한 건과일 여운이 끝없이 이어짐"
        },
        "taste_profile": {
            "단맛(Sweetness)": 8,
            "피트감(Peat)": 1,
            "셰리/과일(Sherry)": 8,
            "오크/나무(Oak)": 7,
            "바디감(Body)": 8
        },
        "current_prices": {
            "대형마트/스마트오더": 330000,
            "남대문/주류상가": 270000,
            "제주/해외면세점": 230000,
            "해외직구(세금포함)": 410000
        },
        "price_history": [360000, 350000, 345000, 340000, 330000, 320000, 310000, 312000, 315000, 320000, 325000, 330000]
    },
    {
        "id": "hibiki_harmony",
        "name_ko": "히비키 재패니즈 하모니",
        "name_en": "Hibiki Japanese Harmony",
        "category": "기타/일본",
        "origin": "일본",
        "abv": 43.0,
        "age": "NAS",
        "image_url": "https://images.unsplash.com/photo-1618260700578-2a6288efd194?auto=format&fit=crop&q=80&w=600",
        "description": "자연과 사람이 조화를 이룬다는 사상 아래 24절기를 의미하는 24면체 크리스탈 병에 담긴 프리미엄 블렌디드 위스키입니다. 치타 그레인과 미즈나라 숙성 야마자키 원액 등이 절묘하게 섞여 들꽃과 꿀처럼 맑고 화사한 풍미를 뿜어냅니다.",
        "tasting_notes": {
            "Nose": "로즈메리, 로즈 꽃잎, 달콤한 멜론, 은은한 미즈나라 오크",
            "Palate": "오렌지 마멀레이드, 화이트 초콜릿의 부드럽고 가벼운 단맛, 정갈한 아카시아 꿀",
            "Finish": "깔끔하고 섬세하며, 오크의 미세한 스파이스와 달콤한 과일 여운"
        },
        "taste_profile": {
            "단맛(Sweetness)": 8,
            "피트감(Peat)": 1,
            "셰리/과일(Sherry)": 7,
            "오크/나무(Oak)": 5,
            "바디감(Body)": 6
        },
        "current_prices": {
            "대형마트/스마트오더": 159000,
            "남대문/주류상가": 132000,
            "제주/해외면세점": 115000,
            "해외직구(세금포함)": 215000
        },
        "price_history": [178000, 172000, 168000, 163000, 159000, 153000, 148000, 149000, 151000, 153000, 156000, 159000]
    },
    {
        "id": "jameson_standard",
        "name_ko": "제임슨 스탠다드",
        "name_en": "Jameson Irish Whiskey",
        "category": "기타/아이리시",
        "origin": "아일랜드",
        "abv": 40.0,
        "age": "NAS",
        "image_url": "https://images.unsplash.com/photo-1628435759132-72c05ad625c2?auto=format&fit=crop&q=80&w=600",
        "description": "전 세계에서 가장 많이 팔리는 정통 아이리시 위스키입니다. 피트를 전혀 사용하지 않아 피트 향이 없고, 대형 단식 증류기에서 3번 증류하여 타의 추종을 불허하는 깔끔함과 고소한 보리 과자 맛을 지녀 하이볼 제조 1순위로 꼽힙니다.",
        "tasting_notes": {
            "Nose": "가볍고 화사한 꽃 향기, 상큼한 배와 연한 바닐라",
            "Palate": "극도로 부드럽고 가벼운 질감, 달콤한 멜론, 고소한 맥아와 약간의 스파이시",
            "Finish": "짧고 깔끔하며 은은한 보리의 구수함과 기분 좋은 달콤함"
        },
        "taste_profile": {
            "단맛(Sweetness)": 6,
            "피트감(Peat)": 1,
            "셰리/과일(Sherry)": 4,
            "오크/나무(Oak)": 3,
            "바디감(Body)": 3
        },
        "current_prices": {
            "대형마트/스마트오더": 32000,
            "남대문/주류상가": 27000,
            "제주/해외면세점": 23000,
            "해외직구(세금포함)": 62000
        },
        "price_history": [34000, 33000, 33000, 32000, 32000, 31000, 30000, 30000, 31000, 31000, 32000, 32000]
    }
]

def get_whisky_dataframe():
    """위스키 원본 리스트를 판다스 데이터프레임으로 변환하여 반환"""
    df = pd.DataFrame(WHISKY_DATA)
    return df

def get_categories():
    """존재하는 위스키 카테고리 목록 반환"""
    return list(set(w["category"] for w in WHISKY_DATA))

def get_origins():
    """위스키 생산지 목록 반환"""
    origins = set()
    for w in WHISKY_DATA:
        country = w["origin"].split("(")[0].strip()
        origins.add(country)
    return list(origins)

def search_whisky(keyword=None, category=None, origin=None, price_range=None):
    """조건에 따른 위스키 필터링 검색"""
    results = WHISKY_DATA
    
    if keyword:
        keyword = keyword.lower()
        results = [w for w in results if keyword in w["name_ko"].lower() or keyword in w["name_en"].lower()]
        
    if category:
        results = [w for w in results if w["category"] == category]
        
    if origin:
        results = [w for w in results if origin in w["origin"]]
        
    if price_range:
        min_p, max_p = price_range
        # 대형마트/스마트오더 가격 기준으로 필터링
        results = [w for w in results if min_p <= w["current_prices"]["대형마트/스마트오더"] <= max_p]
        
    return results

def get_whisky_by_id(whisky_id):
    """ID로 특정 위스키 세부 정보 반환"""
    for w in WHISKY_DATA:
        if w["id"] == whisky_id:
            return w
    return None

def recommend_whiskies(user_preferences, limit=3):
    """
    사용자 선호도(Sweetness, Peat, Sherry, Oak, Body, Price)에 따른 추천 알고리즘
    user_preferences: {
        'Sweetness': 1~10,
        'Peat': 1~10,
        'Sherry': 1~10,
        'Oak': 1~10,
        'Body': 1~10,
        'MaxPrice': int
    }
    """
    scores = []
    
    pref_sweet = user_preferences.get('Sweetness', 5)
    pref_peat = user_preferences.get('Peat', 1)
    pref_sherry = user_preferences.get('Sherry', 5)
    pref_oak = user_preferences.get('Oak', 5)
    pref_body = user_preferences.get('Body', 5)
    max_price = user_preferences.get('MaxPrice', 500000)
    
    for w in WHISKY_DATA:
        # 가격 조건 필터링
        mart_price = w["current_prices"]["대형마트/스마트오더"]
        if mart_price > max_price:
            continue
            
        profile = w["taste_profile"]
        
        # 유클리드 거리를 기반으로 한 유사성 점수 계산 (작을수록 유사)
        distance = np.sqrt(
            (profile["단맛(Sweetness)"] - pref_sweet) ** 2 +
            (profile["피트감(Peat)"] - pref_peat) ** 2 +
            (profile["셰리/과일(Sherry)"] - pref_sherry) ** 2 +
            (profile["오크/나무(Oak)"] - pref_oak) ** 2 +
            (profile["바디감(Body)"] - pref_body) ** 2
        )
        
        # 100점 만점 환산 점수
        # 최대 거리는 sqrt( 5 * (9^2) ) = sqrt(405) ~ 20.12
        max_dist = 20.12
        match_percentage = max(0.0, (1 - (distance / max_dist)) * 100)
        
        scores.append({
            "whisky": w,
            "match_score": round(match_percentage, 1)
        })
        
    # 유사도 높은 순으로 정렬
    scores.sort(key=lambda x: x["match_score"], reverse=True)
    return scores[:limit]

def get_whisky_image_url(whisky):
    """
    로컬 이미지 폴더(whisky_images)에서 
    위스키 ID에 부합하는 이미지 파일(PNG/JPG)이 존재하는지 확인 후, 있으면 로컬 경로를 반환합니다.
    존재하지 않을 경우 기존 Unsplash 고화질 이미지를 반환합니다.
    """
    import os
    local_dir = "whisky_images"
    whisky_id = whisky.get("id")
    if whisky_id and os.path.exists(local_dir):
        for ext in [".png", ".jpg", ".jpeg", ".PNG", ".JPG", ".JPEG"]:
            local_path = os.path.join(local_dir, f"{whisky_id}{ext}")
            if os.path.exists(local_path):
                return local_path
    return whisky['image_url']
