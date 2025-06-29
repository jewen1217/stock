# Stocken Lite v4

AI 기반 주식 분석 + 미래 가격 예측 도구 - OpenRouter LLM 통합

## 주요 특징

🤖 **AI 분석 통합**: OpenRouter API를 통한 고급 LLM 분석  
📊 **기술적 지표**: EMA, MACD, RSI, Bollinger Bands, OBV  
🔄 **실시간 스트리밍**: AI 분석 결과 실시간 출력  
🧠 **멀티 모델**: 5개 최신 AI 모델 동시 분석  
🎯 **신호 추출**: AI 응답에서 자동 매매 신호 추출  
🔮 **미래 예측**: AI 모델들의 1일/3일/1주일/2주일 가격 예측  
📈 **차트 생성**: 과거 30일 + AI 예측 시각화  

## v4 새로운 기능 🆕

### 🔮 AI 가격 예측
- **5개 모델 동시 예측**: Qwen, DeepSeek, Gemini, GPT-4O, Claude Sonnet
- **다양한 예측 기간**: 1일, 3일, 1주일, 2주일 후 가격 예측
- **JSON 구조화 응답**: 신뢰도, 근거, 신호까지 포함된 예측 결과
- **예측 차트**: 과거 30일 데이터 + AI 모델별 미래 예측 라인

### 📊 시각화 강화
- **가격 예측 차트**: 과거 데이터와 AI 예측을 한 눈에 비교
- **요약 테이블**: 모델별 예측 결과 및 신뢰도 비교
- **모델별 색상**: 각 AI 모델을 구분하는 고유 색상 및 마커
- **고해상도 PNG**: 300 DPI 고품질 차트 저장

### 🔧 기술적 개선
- **모듈화 설계**: 5개 독립 모듈로 구성 (chart_generator.py 추가)
- **비동기 처리**: 멀티 모델 분석 최적화
- **JSON 파싱**: AI 응답의 구조화된 데이터 처리
- **matplotlib 통합**: 전문적인 차트 생성

## 파일 구조

```
v4/
├── data_loader.py          # 데이터 수집 모듈
├── technical_analyzer.py   # 기술적 지표 분석 모듈  
├── llm_analyzer.py         # AI 분석 + 가격 예측 모듈 (ENHANCED!)
├── chart_generator.py      # 차트 생성 모듈 (NEW!)
├── main.py                # 실행기 모듈
├── requirements.txt       # 의존성 패키지
└── README.md             # 이 파일
```

## 사용 가능한 AI 모델

### 기본 분석 모델
- **Claude 3.5 Sonnet**: 빠르고 정확한 분석

### 가격 예측 모델 (5개 동시)
1. **Qwen 2.5 72B Instruct**: 중국 알리바바의 최신 모델
2. **DeepSeek Chat v3**: 코딩 특화 고성능 모델  
3. **Google Gemini 2.5 Flash**: 구글의 빠른 멀티모달 모델
4. **GPT-4O**: OpenAI의 최신 모델
5. **Claude 3.5 Sonnet**: 종합 분석 및 예측

## 설치 및 실행

### 의존성 설치
```bash
pip install -r requirements.txt
```

### 실행 방법

#### 1. 대화형 모드 (추천)
```bash
python main.py
```

#### 2. 명령행 모드

##### 기본 기술적 분석
```bash
python main.py AAPL
python main.py 005930 --period 6mo
```

##### AI 분석 (기본)
```bash
python main.py AAPL --llm
python main.py AAPL:llm
```

##### AI 심층 분석 (4개 모델)
```bash
python main.py AAPL --deep
python main.py AAPL:deep
```

##### 🆕 AI 가격 예측 + 차트 (5개 모델)
```bash
python main.py AAPL --predict
python main.py AAPL:predict
```

## 사용 예시

### 1. 기본 기술적 분석
```
python main.py AAPL

=== Stock Analysis for AAPL ===
Date: 2025-06-25
Current Price: 201.56
Volume: 39,454,000
Data Points: 251

--- Technical Indicators ---
EMA: Short(12): 200.09, Long(26): 201.12, Signal: 0 (SELL)
MACD: -1.0376, Signal Line: -1.4146, Histogram: 0.3770, Signal: 1 (BUY)
RSI: 50.60, Signal: 1 (NEUTRAL)
Bollinger Bands: Upper: 204.91, Middle: 200.36, Lower: 195.80, Signal: 0 (SELL)
OBV: 595,878,500, Signal: 1 (STRONG)

--- Summary ---
Composite Signal: -1 (SELL)
Signal Strength: 3/5
```

### 2. AI 기본 분석
```
python main.py AAPL:llm

=== AAPL AI 분석 시작 (Claude 3.5 Sonnet) ===
[기술적 분석 결과 출력]

--- AI 분석 결과 ---
현재 Apple 주식은 매도 신호를 보이고 있습니다. 
단기 EMA가 장기 EMA 아래에 위치하고 있으며, 
RSI는 중립 구간에 있지만 볼린저 밴드 상단 근처에서 
거래되고 있어 단기적인 조정이 예상됩니다...

--- 분석 결과 ---
신호: 매도 (-1)
```

### 3. AI 심층 분석
```
python main.py AAPL:deep

=== AAPL 심층 AI 분석 시작 ===
4개 AI 모델로 종합 분석 중...

--- 모델 1/4: qwen/qwen-2.5-72b-instruct ---
매도 신호입니다. 기술적 지표들이 혼재된 신호를 보이고 있으나...
신호: 매도 (-1)

--- 모델 2/4: deepseek/deepseek-chat-v3-0324 ---
중립 신호입니다. 현재 시점에서는 관망이 적절할 것으로 판단됩니다...
신호: 중립 (0)

--- 모델 3/4: google/gemini-2.5-flash ---
매수 신호입니다. RSI가 중립구간에 있고 OBV가 강세를 보이고 있어...
신호: 매수 (1)

--- 모델 4/4: openai/gpt-4o-2024-11-20 ---
매도 신호입니다. 단기 EMA가 장기 EMA 아래에 있어 약세 추세...
신호: 매도 (-1)

=== 종합 분석 결과 ===
참여 모델: 4/4개
종합 신호: 중립 (0)
개별 신호: [-1, 0, 1, -1]
```

### 4. 🆕 AI 가격 예측 + 차트
```
python main.py AAPL:predict

=== AAPL AI 가격 예측 분석 시작 ===
5개 AI 모델로 미래 가격 예측 + 차트 생성 중...

[기술적 분석 결과 출력]

--- AI 가격 예측 시작 ---
각 모델이 1일/3일/1주일/2주일 후 가격을 예측 중...

=== AI 가격 예측 결과 ===
현재 가격: $201.56
예측 모델: 5개 (Qwen, DeepSeek, Gemini, GPT-4O, Claude)

🤖 Qwen 2.5 72B:
   신호: 매수 (신뢰도: 0.75)
   1일 후: $203.20 (+0.8%)
   3일 후: $205.80 (+2.1%)
   1주일 후: $208.50 (+3.4%)
   2주일 후: $212.00 (+5.2%)
   근거: 기술적 지표 개선과 거래량 증가 등...

🤖 DeepSeek Chat:
   신호: 중립 (신뢰도: 0.68)
   1일 후: $200.90 (-0.3%)
   3일 후: $202.10 (+0.3%)
   1주일 후: $203.80 (+1.1%)
   2주일 후: $205.20 (+1.8%)
   근거: 혼재된 기술적 신호로 인한 횡보 전망...

... (기타 모델 예측)

성공한 예측: 5/5개 모델
✅ 충분한 모델이 예측을 완료했습니다.

--- 차트 생성 중 ---

✅ 분석 완료!
🔮 5개 AI 모델의 가격 예측이 완료되었습니다.
📊 차트가 생성되었습니다: AAPL_prediction_chart_20250626_143052.png
```

## 대화형 모드 사용법

```
=== Stocken Lite v4 - AI 주식 분석 + 가격 예측 도구 ===
종료하려면 'quit', 'exit', 또는 'q'를 입력하세요.
도움말을 보려면 'help'를 입력하세요.
🔮 새로운 기능: AI 가격 예측 + 차트!

분석 옵션:
  기본: AAPL (기술적 분석)
  AI: AAPL:llm (Claude 분석)
  심층: AAPL:deep (4개 모델 분석)
  🆕 예측: AAPL:predict (5개 모델 가격 예측 + 차트)

주식 코드를 입력하세요 (예: AAPL, AAPL:predict, AAPL:deep): AAPL:predict
```

## 신호 해석

### 기술적 지표 신호
- **EMA**: 단기선이 장기선 위에 있으면 BUY, 아래에 있으면 SELL
- **MACD**: MACD가 시그널선 위에 있으면 BUY, 아래에 있으면 SELL  
- **RSI**: 30-70 구간이면 NEUTRAL, 과매수/과매도 구간이면 WARNING
- **Bollinger Bands**: 하단 밴드 근처나 돌파시 BUY, 그 외 SELL
- **OBV**: 5일 평균보다 높으면 STRONG, 낮으면 WEAK

### AI 분석 신호
- **강력 매수 (2)**: 매우 강한 매수 신호
- **매수 (1)**: 매수 신호
- **중립 (0)**: 중립/보유 신호
- **매도 (-1)**: 매도 신호
- **강력 매도 (-2)**: 매우 강한 매도 신호

### 종합 신호 (기술적 분석)
- **BUY (1)**: 모든 5개 지표가 동시에 매수 신호
- **SELL (-1)**: 하나라도 매도 조건 충족  
- **HOLD (0)**: 위 조건에 해당하지 않음

## 버전별 비교

| 기능 | v1 | v2 | v3 | v4 |
|------|----|----|----|----|
| 파일 구조 | 단일 파일 | 3개 모듈 | 4개 모듈 | 5개 모듈 |
| AI 분석 | ❌ | ❌ | ✅ | ✅ |
| 기본 LLM | ❌ | ❌ | ✅ Claude 3.5 | ✅ Claude 3.5 |
| 심층 분석 | ❌ | ❌ | ✅ 4개 모델 | ✅ 4개 모델 |
| 🆕 가격 예측 | ❌ | ❌ | ❌ | ✅ 5개 모델 |
| 🆕 차트 생성 | ❌ | ❌ | ❌ | ✅ matplotlib |
| 🆕 JSON 파싱 | ❌ | ❌ | ❌ | ✅ 구조화 응답 |
| 스트리밍 | ❌ | ❌ | ✅ 실시간 | ✅ 실시간 |
| 신호 추출 | ❌ | ❌ | ✅ 자동 | ✅ 자동 |
| 비동기 처리 | ❌ | ❌ | ✅ | ✅ |
| 도움말 | ❌ | ✅ | ✅ 향상됨 | ✅ 완전판 |

## API 설정

OpenRouter API 키가 필요합니다. `llm_analyzer.py`에서 설정하거나 환경변수로 설정 가능합니다.

```python
# llm_analyzer.py에서 직접 설정 (현재 기본값 사용)
self.api_key = "your-api-key-here"

# 또는 환경변수 사용
export OPENROUTER_API_KEY="your-api-key-here"
```

## 주의사항

- AI 분석은 인터넷 연결이 필요합니다
- OpenRouter API 사용료가 발생할 수 있습니다
- 가격 예측 분석은 시간이 오래 걸립니다 (3-8분)
- 차트 파일은 현재 디렉토리에 PNG 형식으로 저장됩니다
- AI 분석 및 가격 예측 결과는 참고용이며 투자 결정에 신중하게 사용하세요
- 미래 가격 예측은 다양한 외부 요인으로 인해 실제와 다를 수 있습니다

## 개발자 정보

- **버전**: 4.0
- **기반**: Stocken v16 알고리즘
- **언어**: Python 3.7+
- **AI 제공**: OpenRouter API
- **주요 의존성**: pandas, numpy, finance-datareader, requests, aiohttp, matplotlib

## 차트 기능 상세

### 생성되는 차트 파일
1. **가격 예측 차트**: `{SYMBOL}_prediction_chart_{TIMESTAMP}.png`
   - 과거 30일 주가 데이터 (검은 실선)
   - 현재 가격 강조 (빨간 점)
   - 5개 모델의 미래 예측 라인 (각기 다른 색상)
   - 예측 포인트별 마커 (1일/3일/1주일/2주일)

2. **요약 테이블**: `{SYMBOL}_prediction_summary_{TIMESTAMP}.png`
   - 모델별 신호 및 신뢰도
   - 기간별 예측 가격 및 변화율
   - 각 모델의 예측 근거 요약

### 차트 특징
- **고해상도**: 300 DPI PNG 형식
- **모델별 색상 구분**: 각 AI 모델마다 고유 색상
- **예측 기간별 마커**: 다양한 모양으로 기간 구분
- **신뢰도 반영**: 신뢰도에 따른 투명도 조절

---

💡 **v4 Tip**: 
1. 기술적 분석으로 현재 상황 파악
2. AI 심층 분석으로 종합 의견 확인
3. 🆕 가격 예측으로 미래 전망 및 차트 확인
4. 생성된 차트로 시각적 분석 완료!