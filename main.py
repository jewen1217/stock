import argparse
import sys
import pandas as pd
from data_loader import DataLoader
from technical_analyzer import TechnicalAnalyzer
# from llm_analyzer import LLMAnalyzer
# from chart_generator import ChartGenerator
from typing import Optional


class StockAnalysisApp:
    """
    주식 기술적 분석 애플리케이션 메인 클래스
    """
    
    def __init__(self):
        self.data_loader = DataLoader()
        self.analyzer = TechnicalAnalyzer()
        # self.llm_analyzer = LLMAnalyzer()
        # self.chart_generator = ChartGenerator()
    
    def format_signal(self, signal_value: int, positive_label: str = "BUY", negative_label: str = "SELL") -> str:
        """
        신호 값을 라벨과 함께 포맷팅합니다.
        
        Args:
            signal_value (int): 신호 값 (0 또는 1)
            positive_label (str): 양수 신호 라벨
            negative_label (str): 음수 신호 라벨
            
        Returns:
            str: 포맷된 신호 문자열
        """
        if signal_value == 1:
            return f"{signal_value} ({positive_label})"
        elif signal_value == 0:
            return f"{signal_value} ({negative_label})"
        else:
            return f"{signal_value} (NEUTRAL)"
    
    def print_analysis(self, result: dict):
        """
        분석 결과를 포맷팅하여 출력합니다.
        
        Args:
            result (dict): 분석 결과
        """
        if "error" in result:
            print(f"Error: {result['error']}")
            return
        
        print(f"\n=== Stock Analysis for {result['symbol']} ===")
        
        # 날짜 포맷팅
        date_str = result['date']
        if hasattr(result['date'], 'strftime'):
            date_str = result['date'].strftime('%Y-%m-%d')
        
        print(f"Date: {date_str}")
        print(f"Current Price: {result['price']:.2f}")
        print(f"Volume: {result['volume']:,}")
        print(f"Data Points: {result['data_points']}")
        
        print(f"\n--- Technical Indicators ---")
        ti = result['technical_indicators']
        
        # 각 지표별 출력
        print(f"EMA: Short({self.analyzer.SHORT_EMA_PERIOD}): {ti['EMA']['short']:.2f}, "
              f"Long({self.analyzer.LONG_EMA_PERIOD}): {ti['EMA']['long']:.2f}, "
              f"Buy: {ti['EMA']['buy']}, Sell: {ti['EMA']['sell']}")
        
        print(f"MACD: {ti['MACD']['macd']:.4f}, Signal Line: {ti['MACD']['signal_line']:.4f}, "
              f"Histogram: {ti['MACD']['histogram']:.4f}, "
              f"Buy: {ti['MACD']['buy']}, Sell: {ti['MACD']['sell']}")
        
        print(f"RSI: {ti['RSI']['value']:.2f}, "
              f"Buy: {ti['RSI']['buy']}, Sell: {ti['RSI']['sell']}")
        
        print(f"Bollinger Bands: Upper: {ti['Bollinger_Bands']['upper']:.2f}, "
              f"Middle: {ti['Bollinger_Bands']['middle']:.2f}, "
              f"Lower: {ti['Bollinger_Bands']['lower']:.2f}, "
              f"Buy: {ti['Bollinger_Bands']['buy']}, Sell: {ti['Bollinger_Bands']['sell']}")
        
        print(f"OBV: {ti['OBV']['value']:,.0f}, "
              f"Buy: {ti['OBV']['buy']}, Sell: {ti['OBV']['sell']}")
        
        print(f"\n--- Summary ---")
        print(f"Buy: {result['buy']}")
        print(f"Sell: {result['sell']}")
        print(f"Buy Strength: {result['buy_strength']}/5")
        print(f"Sell Strength: {result['sell_strength']}/5")
    
    def analyze_single_stock(self, symbol: str, period: str = '1y'):
        """
        단일 주식을 분석합니다.
        
        Args:
            symbol (str): 주식 심볼
            period (str): 분석 기간
        """
        # 데이터 로드
        df = self.data_loader.fetch_stock_data(symbol, period)
        if df is None:
            return
        
        # 기술적 분석 수행
        result = self.analyzer.analyze_stock(df, symbol)
        
        # 결과 출력
        self.print_analysis(result)
    
    
    def run_interactive_mode(self, period: str = '1y'):
        """
        대화형 모드로 실행합니다.
        
        Args:
            period (str): 분석 기간
        """
        print("도움말을 보려면 'help'를 입력하세요.")
        
        while True:
            try:
                user_input = input("\n주식 코드를 입력하세요 (예: AAPL): ").strip()
                # LLM 분석 옵션 파싱
                symbol = user_input
                analysis_type = 'basic'
                backtest_date = None
                if ':' in user_input:
                    parts = user_input.split(':')
                    symbol = parts[0].strip()
                    if len(parts) > 1:
                        analysis_type = parts[1].strip().lower()
                    if len(parts) > 2:
                        backtest_date = parts[2].strip()
                if not symbol:
                    print("주식 코드를 입력해주세요.")
                    continue
                if symbol.lower() in ['quit', 'exit', 'q']:
                    print("프로그램을 종료합니다.")
                    break
                if symbol.lower() == 'help':
                    self.show_help()
                    continue
                self.analyze_single_stock(symbol, period)
            except KeyboardInterrupt:
                print("\n프로그램을 종료합니다.")
                break
            except Exception as e:
                print(f"오류가 발생했습니다: {e}")
                continue
    
    def show_help(self):
        """
        도움말을 출력합니다.
        """
        print("\n=== 도움말 ===")
        print("사용 가능한 명령어:")
        print("  - 주식 코드 입력: AAPL, 005930 등 (기술적 분석)")
        print("  - help: 이 도움말 표시")
        print("  - quit/exit/q: 프로그램 종료")
        print("\n기간 옵션 (--period):")
        print("  - 1d, 5d: 단기")
        print("  - 1mo, 3mo, 6mo: 월 단위")
        print("  - 1y, 2y, 5y, 10y: 년 단위")
        print("  - ytd: 연초부터")
        print("  - max: 최대 기간")
        
        explanations = self.analyzer.get_signal_explanation()
        print("\n=== 기술적 지표 신호 설명 ===")
        for indicator, explanation in explanations.items():
            print(f"  - {indicator}: {explanation}")
        


def main():
    """
    메인 함수
    """
    parser = argparse.ArgumentParser(description='Stock Technical Analysis Tool')
    parser.add_argument('symbol', nargs='?', help='Stock symbol to analyze (e.g., AAPL, 005930)')
    parser.add_argument('--period', default='1y', 
                       help='Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)')
    
    args = parser.parse_args()
    
    # 앱 인스턴스 생성
    app = StockAnalysisApp()
    
    # 심볼이 주어진 경우 단일 분석 모드
    if args.symbol:
        # 심볼에서 분석 타입 파싱
        symbol = args.symbol
        analysis_type = 'basic'
        backtest_date = None
        if ':' in args.symbol:
            parts = args.symbol.split(':')
            symbol = parts[0].strip()
            if len(parts) > 1:
                analysis_type = parts[1].strip().lower()
            if len(parts) > 2:
                backtest_date = parts[2].strip()
        # 분석 수행
        app.analyze_single_stock(symbol, args.period)
    else:
        # 대화형 모드
        app.run_interactive_mode(args.period)


if __name__ == "__main__":
    main()